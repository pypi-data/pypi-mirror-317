"""Provide protocol for tokens."""
from __future__ import annotations

from dataclasses import InitVar, dataclass, field
from enum import Enum
from typing import Any, Protocol, Self

if __name__ == "__main__" and not __package__:  # pragma: no cover
    from pathlib import Path
    from sys import path

    path.append(str(Path(__file__).parent.parent.parent))


class TokenProtocol[TerminalType: Enum](Protocol):
    """A token must implement all these attributes in order to be used with the library.

    However, if there is no special handling of lines and this information can be discarded, there is no need \
        to implement start_line, stop_line, start_column, and stop_column, the implementation in this class can be used.
    extended_token_type also doesn't need to be implemented if not needed.
    """

    def __hash__(self) -> int:
        """Different contents have different hashs."""
        return hash((
            self.token_type,
            self.start_position,
            self.stop_position,
            self.content,
        ))

    @property
    def token_type(self) -> TerminalType:
        """Type of the token."""
        raise NotImplementedError

    @property
    def start_position(self) -> int:
        """Index of the first character of the token in the input."""
        raise NotImplementedError
    @property
    def stop_position(self) -> int:
        """Index of the last character of the token + 1 in the input."""
        raise NotImplementedError

    @property
    def content(self) -> str:
        """String content of the token."""
        raise NotImplementedError

class TokenWithFrozenDataProtocol[
    TerminalType: Enum,
    TokenDataType,
](TokenProtocol[TerminalType], Protocol):
    """Token that has a readable(-only or not) data attribute."""

    @property
    def data(self) -> TokenDataType:
        """User defined data attribute."""
        raise NotImplementedError

class TokenWithMutableDataProtocol[
    TerminalType: Enum,
    TokenDataType,
](TokenProtocol[TerminalType], Protocol):
    """Token with mutable data attribute."""

    data: TokenDataType

class TokenWithPositionProtocol[TokenTypeType_co: Enum](TokenProtocol[TokenTypeType_co], Protocol):
    """Token that has columns and lines positions."""

    @property
    def start_line(self) -> int:
        r"""Number of \n characters before the first character if the token."""
        raise NotImplementedError

    @property
    def stop_line(self) -> int:
        r"""Start line increased of the number of \n in the token."""
        raise NotImplementedError

    @property
    def start_column(self) -> int:
        r"""Number of non newline characters between the first character of this token and the first \n before it.

        So the first character of a line, right after a \n or the first character of a file, has a start_column of 0.
        """
        raise NotImplementedError

    @property
    def stop_column(self) -> int:
        r"""Number of non newline characters between the last character of this token and the first \n before it.

        Therefore, if a token ends with a \n and the previous character is not a \n, stop_column will be nonzero.
        """
        raise NotImplementedError

class ClassicalTokenProtocol[TerminalType: Enum, TokenDataType](
    TokenWithPositionProtocol[TerminalType],
    TokenWithFrozenDataProtocol[TerminalType, TokenDataType],
    Protocol,
):
    """Token with lines and column positions, and data attribute."""

    pass  # noqa: PIE790 pylint: disable=unnecessary-pass

@dataclass
class BaseToken[TerminalType, TokenDataType]:
    """Minimal dataclass token implementing ClassicalTokenProtocol."""

    token_type: TerminalType

    content: str

    start_position: int
    stop_position: int

    start_line: int
    stop_line: int
    start_column: int
    stop_column: int

    data: TokenDataType


@dataclass
class AutoCalculatingToken[TerminalType: Enum, TokenDataType]:
    """When every character of the input is part of a Token."""

    token_type: TerminalType

    content: str

    start_position: int
    stop_position: int

    previous: InitVar[Self | None]

    data: TokenDataType
    start_line: int = field(init=False)
    stop_line: int = field(init=False)
    start_column: int = field(init=False)
    stop_column: int = field(init=False)

    def __post_init__(self, previous: Self | None) -> None:
        """Calculate start_line, stop_line, start_column, and stop_column."""
        assert self.start_position is not None
        assert self.stop_position is not None
        if previous is None:
            self.start_line = 0
            self.start_column = 0
        else:
            assert hasattr(previous, "start_line")
            self.start_column = previous.stop_column
            self.start_line = previous.stop_line
        try:
            self.stop_column = self.content[::-1].index("\n")
        except ValueError:
            self.stop_column = len(self.content) + self.start_column
        self.stop_line = self.start_line + self.content.count("\n")
        previous = None

    __hash__ = TokenProtocol[TerminalType].__hash__

    def __reduce__(self) -> str | tuple[Any, ...]:
        """When unpickling AutoCalculatingToken, the lines and columns are directly restored. Previous is not used."""
        return (
            AutoCalculatingToken,
            (
                self.token_type,
                self.content,
                self.start_position,
                self.stop_position,
                # self.previous,
                None,
                self.data,
            ),
            {
                "start_line": self.start_line,
                "stop_line": self.stop_line,
                "start_column": self.start_column,
                "stop_column": self.stop_column,
            },
        )
