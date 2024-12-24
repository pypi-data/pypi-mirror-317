"""Produce a token list from a str."""

from __future__ import annotations

import weakref
from itertools import count
from pathlib import Path
from typing import Any, cast

from cffi import FFI  # type: ignore

#########################################################
#########################################################
# Global parameters


COMPLETE_SHARED_LIBRARY: str = "complete.shared"


#########################################################
#########################################################
def generate_ffi() -> FFI:
    """Produce the ffi for the shared library built from tokenizer.c++.

    The C/C++ parsing time can be significant for small inputs.
    """
    ffi = FFI()  # pylint: disable=W0621
    ffi.cdef("""
        long *getContiguousArray(void *v);
    """)
    ffi.cdef("""
        void *sqlite3_complete(const char *zSql);
    """)
    ffi.cdef("""
        void free_complete_list(void *completeList);
    """)
    return ffi


class Globals:  # noqa: D101
    def __init__(self) -> None:  # type: ignore
        """Init CFFI and stores state in a Globals object."""
        self.ffi: FFI = generate_ffi()
        folder = Path(__file__).parent / "libs"
        try:
            from os import add_dll_directory
        except ImportError:  # pragma: no cover
            self.lib: Any = self.ffi.dlopen(str(folder / COMPLETE_SHARED_LIBRARY))
        else:
            with add_dll_directory(str(folder.absolute())):
                from ctypes import CDLL

                path = str(folder.absolute() / COMPLETE_SHARED_LIBRARY)
                CDLL(path, winmode=0)
                self.lib: Any = self.ffi.dlopen(path)


def init_module() -> None:
    """Init CFFI and stores state in a Globals object.

    Other context objects can be supplied using g arguments in sqlite3_complete_Binding.
    """
    assert getattr(init_module, "g", None) is None
    init_module.g = Globals()  # type: ignore


def sqlite3_complete_Binding(  # noqa: N802
    encoded: bytes,
    *,
    g: Globals | None = None,
) -> list[int]:  # pylint: disable=C0103
    """Return a list of tuple containing position, length, TokenType and ETokenType."""
    g = g or cast(Globals, init_module.g)  # type: ignore
    assert g.ffi is not None
    assert g.lib is not None
    argument = g.ffi.new("char[]", encoded)
    ret = g.lib.sqlite3_complete(argument)
    _ = weakref.finalize(ret, g.lib.free_complete_list, ret)
    data = g.lib.getContiguousArray(ret)
    result: list[int] = []
    for i in count():  # pragma: no branch
        index = data[i]
        if index == -1:
            break
        result.append(index)
    return result


init_module()
