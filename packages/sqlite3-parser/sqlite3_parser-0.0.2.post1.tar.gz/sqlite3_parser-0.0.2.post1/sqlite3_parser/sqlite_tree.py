"""Specialized Tree for SQLite ASTs."""
from __future__ import annotations

from functools import cached_property
from re import fullmatch
from typing import Any, cast

from parser.tree.classic_tree import ClassicTree
from parser.tree.protocols import ClassicalTokenProtocol
from parser.tree.tree import duck_copy
from parser.tree.tree_auxiliary import ContentMatch

from .rules import RulesTypes
from .tokenizer import ETokenType, TokenType


class SQLiteTree(ClassicTree[TokenType, RulesTypes, None, None, tuple[ETokenType, Any]]):
    """Tree for SQLite with ability to match search within -- comments."""

    @cached_property
    def regexable_left_individual_ddash_comments(
        self,
    ) -> ContentMatch[TokenType, RulesTypes, None, None]:
        r"""Case sensitive.

        \n is appended at the end of each individual comment content.
        Terminate your pattern with it to make it a fullmatch, as there is only one \n in each content.
        """
        return ContentMatch(
            self.subtree_ddash_extraction_function,
            self,
            case_sensitive=True,
            regex_function=fullmatch,
            iterable_content=True,
        )

    @cached_property
    def subtree_ddash_extraction_function(
        self,
    ) -> list[str]:
        """Return the previous ddash -- comments with appended newline at each one, up to the next non whitespace comment."""
        left: list[str] = []
        tkl = cast(
            tuple[ClassicalTokenProtocol[TokenType, tuple[ETokenType, Any]], ...],
            self.tree_attributes.script_context.token_list,
        )
        for token in tkl[:self.tokens_bounds.start][::-1]:
            if token.token_type != TokenType.TK_SPACE:
                break
            if token.data[0] == ETokenType.DOUBLE_DASH_COMMENT:
                left.append(f"{token.content}\n")
        return left[::-1]

    @staticmethod
    def duck_copy(  # type: ignore
        root_or_subroot: ClassicTree[TokenType, RulesTypes, None, None, tuple[ETokenType, Any]],
        *,
        top_caller: bool = True,
        deep_copy_node_data: bool = False,
    ) -> SQLiteTree:
        """Perform an efficient duck copy."""
        return duck_copy(
            self=root_or_subroot,
            deep_copy_node_data=deep_copy_node_data,
            cls=SQLiteTree,
            top_caller=top_caller,
        )

    __match_args__ = (
        "element",
        "has_unordered_elements_in_descendants",
        "regexable_content",
        "has_unordered_ancestors_rulestypes",
        "regexable_ignored_content",
        "lines",
        "match_total_children_number",
        "children",
        "match_direct_children_number",
        "match_active_token_content",
        "regexable_left_individual_ddash_comments",
    )
