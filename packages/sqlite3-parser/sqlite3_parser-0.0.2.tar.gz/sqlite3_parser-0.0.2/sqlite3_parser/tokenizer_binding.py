"""Binding to adapted SQLite C tokenizer."""

from __future__ import annotations

import weakref
from itertools import count
from pathlib import Path
from typing import Any, cast

from cffi import FFI  # type: ignore

from .terminals import (
    ETokenType,
    TokenType,
    e_token_conversion_table,
    token_conversion_table,
)

#########################################################
#########################################################
# Global parameters


TOKENIZE_SHARED_LIBRARY = "tokenize.shared"


#########################################################
#########################################################


def generate_ffi() -> FFI:
    """Produce the ffi for the shared library built from tokenizer.c++."""
    ffi = FFI()  # pylint: disable=W0621
    ffi.cdef("""
    typedef enum {
    noInfo = 0,
    doubleDashComment
    }ExtendedTokenTypes;
    """)
    ffi.cdef("""
    typedef struct {
        size_t position;
        size_t length;
        int token;
        ExtendedTokenTypes eToken;
    }Token;
    """)
    ffi.cdef("""
    Token* tokenizeFileCallerCallFree(const unsigned char *zIn);
    """)
    ffi.cdef("""void fw(void* data);""")
    return ffi


class Globals:
    """Initialize FFI and library."""

    def __init__(self) -> None:
        """Instanciate FFI, parse C definitions and open shared library."""
        self.ffi: FFI = generate_ffi()
        folder = Path(__file__).parent / "libs"
        try:
            from os import add_dll_directory
        except ImportError:  # pragma: no cover
            self.lib: Any = self.ffi.dlopen(str(folder / TOKENIZE_SHARED_LIBRARY))
        else:
            with add_dll_directory(str(folder.absolute())):
                from ctypes import CDLL

                path = str((folder / TOKENIZE_SHARED_LIBRARY).absolute())
                CDLL(path, winmode=0)
                self.lib: Any = self.ffi.dlopen(path)


def init_module() -> None:
    """Instanciate FFI, parse C definitions and open shared library."""
    assert getattr(init_module, "g", None) is None
    init_module.g = Globals()  # type: ignore


def tokenize_file_Binding(  # noqa: N802 pylint: disable=C0103
    encoded_str: bytes,
    *,
    g: Globals | None = None,
) -> list[tuple[int, int, TokenType, ETokenType]]:
    """Return a list of tuple containing position, length, TokenType and ETokenType."""
    g = g or cast(Globals, init_module.g)  # type: ignore
    argument = g.ffi.new("char[]", encoded_str)
    ret = g.lib.tokenizeFileCallerCallFree(argument)
    _ = weakref.finalize(ret, g.lib.fw, ret)
    result: list[tuple[int, int, TokenType, ETokenType]] = []
    for i in count():  # pragma: no branch
        r = ret[i]
        position = r.position
        if position == 0 and r.length == 0 and r.token == 0 and e_token_conversion_table[r.eToken] == ETokenType.NO_INFO:
            break
        result.append(
            (
                position,
                r.length,
                token_conversion_table[r.token - 1],
                cast(ETokenType, e_token_conversion_table[r.eToken]),
            ),
        )
    return result


init_module()

__all__ = [
    "tokenize_file_Binding",
]
