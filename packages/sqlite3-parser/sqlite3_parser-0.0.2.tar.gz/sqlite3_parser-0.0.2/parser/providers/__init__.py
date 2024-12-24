"""Provider protocol."""

from __future__ import annotations

from collections.abc import Iterable
from enum import Enum
from typing import Protocol

from parser.script_context import ScriptContext
from parser.tree.classic_tree import ClassicalTokenProtocol, ClassicTree


class Provider[TerminalType: Enum, RulesType: Enum](Protocol):
    """Create a parser from a given Lark grammar, then use it to parse a list of tokens."""

    def __init__(
        self,
        grammar: str,
        rules_enum: type[RulesType],
    ) -> None:
        """Create the lark.Lark object with the given grammar and PassThroughLexer."""
        raise NotImplementedError

    def parse[TokenDataType](
        self,
        active_tokens_list: Iterable[ClassicalTokenProtocol[TerminalType, TokenDataType]],
        script_context: ScriptContext[TerminalType],
        active_token_chunk_bounds: slice,
    ) -> ClassicTree[TerminalType, RulesType, None, None, TokenDataType]:
        """Parse the given token list (not str).

        active_tokens_list is passed just to infer eventual data existance.
        """
        raise NotImplementedError

__all__ = [
    "Provider",
]
