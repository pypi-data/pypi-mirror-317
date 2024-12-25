"""Helper module for tests or quickly using the grammar."""

from __future__ import annotations

import typing
from dataclasses import dataclass
from pathlib import Path

from parser.memoize import CachingParser
from parser.providers.lark import LarkParser
from parser.script_context import ScriptContext
from parser.tree.protocols import AutoCalculatingToken

from .cutter import get_valid_split_indexes
from .encoding import get_unicode_offsets_and_encoded_str
from .grammar import grammar
from .rules import RulesTypes
from .sqlite_tree import SQLiteTree
from .terminals import ETokenType, TokenType, ignored_tokens
from .tokenizer import tokenize


def get_script_context(
    script: str,
) -> tuple[ScriptContext[TokenType], dict[int, int], bytes, list[int]]:
    """Obtain script_context, unicode_offsets and encoded_str from a str, and optionally valid_split_indexes."""
    unicode_offsets, encoded_str = get_unicode_offsets_and_encoded_str(script)
    token_list = tuple(tokenize(encoded_str, unicode_offsets))
    script_context = ScriptContext(script, token_list, ignored_tokens)
    return (
        script_context,
        unicode_offsets,
        encoded_str,
        get_valid_split_indexes(script_context, unicode_offsets, encoded_str),
    )


def simple_parse(s: str) -> SQLiteTree:
    """Parse the given script."""
    parser: LarkParser[TokenType, RulesTypes] = LarkParser(grammar, RulesTypes)
    script_context: ScriptContext[TokenType]
    script_context, _, _, _ = get_script_context(s)
    classic_tree = parser.parse(
        typing.cast(tuple[AutoCalculatingToken[TokenType, tuple[ETokenType, typing.Any]]], script_context.active_token_list),
        script_context,
        slice(0, len(script_context.active_token_list)),
    )
    ret: SQLiteTree = SQLiteTree.duck_copy(classic_tree)
    ret.check()
    return ret


class SQLiteParser:
    """Parser with a cache."""

    def __init__(
        self,
        cache_path: str | None | Path,
        max_cache_size: int = 1 << 26,
    ) -> None:
        """Pass None as cache_path to use in memory cache. Otherwise pass path to cache file to user."""
        lp: LarkParser[TokenType, RulesTypes] = LarkParser(
            grammar,
            RulesTypes,
        )
        self.parser: CachingParser[TokenType, tuple[ETokenType, typing.Any], RulesTypes] = CachingParser(
            lp,
            [],
            cache_path,
            max_cache_size,
        )

    def parse(self, script: str) -> SQLiteFullParseResultType:
        """Parse the given script, cutting it in chuck, and using memoization with a cache."""
        scs = get_script_context(script)
        fpr = self.parser(
            scs[0],
            scs[3],
            pop_last_empty_if_s_non_empty=True,
        )
        return SQLiteFullParseResultType(
            SQLiteTree.duck_copy(fpr.rebuilt_parse_tree),
            fpr.rebuilt_parse_tree_sc,
            fpr.leftover_left,
            fpr.leftover_right,
            fpr.left_token_leftover,  # type: ignore
            fpr.right_token_leftover,  # type: ignore
        )


@dataclass
class SQLiteFullParseResultType:
    """Contain all the results obtained during treatment of a string, including parse tree(s)."""

    rebuilt_parse_tree: SQLiteTree
    rebuilt_parse_tree_sc: ScriptContext[TokenType]  # Script context
    leftover_left: str
    leftover_right: str
    left_token_leftover: tuple[AutoCalculatingToken[TokenType, ETokenType], ...]
    right_token_leftover: tuple[AutoCalculatingToken[TokenType, ETokenType], ...]
