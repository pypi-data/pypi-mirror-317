"""Implements ClassicTree, adding start and stop columns attributes to node."""

from __future__ import annotations

from typing import Literal, cast

from parser.tree.protocols import ClassicalTokenProtocol
from parser.tree.tree import (
    Any,
    DynamicMatchAttributeHelper,
    Enum,
    Self,
    Tree,
    TreeAttributes,
    _NotSet,
    _NotSetType,
    cached_property,
    duck_copy,
)


class ClassicTree[
    TerminalType: Enum,
    RuleType: Enum,
    TreeDataType,
    NodeDataType,
    TokenDataType_co,
](  # pylint: disable=W0223
    Tree[TerminalType, RuleType, TreeDataType, NodeDataType],
):
    """Tree with columns and lines, and token with data attribute."""

    def __init__(  # pylint: disable=W0231  # noqa: D107, PLR0913
        self,
        tree_attributes: TreeAttributes[TerminalType, TreeDataType],
        token: ClassicalTokenProtocol[TerminalType, TokenDataType_co] | None | _NotSetType = _NotSet,
        rule: RuleType | None | _NotSetType = _NotSet,
        children: list[Self] | None = None,
        parent: Self | None | _NotSetType = _NotSet,
        active_tokens_bounds: slice | _NotSetType = _NotSet,
        node_data: NodeDataType | None = None,
        **kwargs: Any,
    ) -> None: raise NotImplementedError

    del __init__

    @cached_property
    def enclosing_token_pair(  # noqa: D102
        self,
    ) -> (
        tuple[
            ClassicalTokenProtocol[TerminalType, TokenDataType_co],
            ClassicalTokenProtocol[TerminalType, TokenDataType_co],
        ] |
        tuple[
            ClassicalTokenProtocol[TerminalType, TokenDataType_co],
            Literal["right", "left"],
        ] |
        Literal[0]
    ):
        raise NotImplementedError
    del enclosing_token_pair
    @cached_property
    def token(self) -> ClassicalTokenProtocol[TerminalType, TokenDataType_co] | None:  # noqa: D102
        raise NotImplementedError
    del token

    @cached_property
    def token_content(self) -> tuple[ClassicalTokenProtocol[TerminalType, TokenDataType_co], ...]:  # noqa: D102
        raise NotImplementedError
    del token_content

    @cached_property
    def active_token_content(self) -> tuple[ClassicalTokenProtocol[TerminalType, TokenDataType_co], ...]:  # noqa: D102
        raise NotImplementedError
    del active_token_content

    @cached_property
    def ignored_token_content(self) -> tuple[ClassicalTokenProtocol[TerminalType, TokenDataType_co], ...]:  # noqa: D102
        raise NotImplementedError
    del ignored_token_content

    @cached_property
    def left_ignored_token(self) -> tuple[ClassicalTokenProtocol[TerminalType, TokenDataType_co], ...]:
        """Ignored tokens preceding the subtree, until the first active token."""
        raise NotImplementedError
    del left_ignored_token

    @cached_property
    def start_line(self) -> int:
        """Get the start line of this tree in the input text."""
        match self.enclosing_token_pair:
            case tuple([token, "left"]):
                return token.start_line
            case tuple([token, "right"]):
                return token.stop_line
            case tuple() as ep:
                start_token, _ = ep
                return start_token.start_line
            case 0:
                return 0
            case _: raise NotImplementedError  # noqa: E701

    @cached_property
    def stop_line(self) -> int:
        """Get the end line of this tree in the input text."""
        match self.enclosing_token_pair:
            case tuple([token, "left"]):
                return token.start_line
            case tuple([token, "right"]):
                return token.stop_line
            case tuple() as ep:
                _, stop_token = ep
                assert not isinstance(stop_token, str)
                return stop_token.stop_line
            case 0:
                return 0
            case _: raise NotImplementedError  # noqa: E701

    @cached_property
    def start_column(self) -> int:
        """Get the start column of this tree in the input text."""
        match self.enclosing_token_pair:
            case tuple([token, "left"]):
                return token.start_column
            case tuple([token, "right"]):
                return token.stop_column
            case tuple() as ep:
                start_token, _ = ep
                return start_token.start_column
            case 0:
                return 0
            case _: raise NotImplementedError  # noqa: E701

    @cached_property
    def stop_column(self) -> int:
        """Get the end column of this tree in the input text."""
        match self.enclosing_token_pair:
            case tuple([token, "left"]):
                return token.start_column
            case tuple([token, "right"]):
                return token.stop_column
            case tuple() as ep:
                _, stop_token = ep
                assert not isinstance(stop_token, str)
                return stop_token.stop_column
            case 0:
                return 0
            case _: raise NotImplementedError  # noqa: E701

    @cached_property
    def lines(self) -> DynamicMatchAttributeHelper:
        """Match if the given line contains part of node's content, or is adjacent to a newline part of the node's content.

        If two lines are given, the start and endline should be exactly these two numbers.

        If there is no columns and lines coordinates, fallback on positions.
        The difference is that if it is a tuple (not a slice), \
            the content should be between caracters at the indexes (but doesn't have to up to those bounds).
        """

        def _condition(value: object) -> bool:
            match value:
                case int():
                    return self.start_line <= value <= self.stop_line
                case tuple(["min", int(min_)]):
                    return self.start_line == min_
                case tuple(["max", int(max_)]):
                    return self.stop_line == max_
            raise TypeError

        return DynamicMatchAttributeHelper(_condition)

    def _check_positions(self) -> None:
        assert self.start_line <= self.stop_line
        _ = self.start_column
        _ = self.stop_column
        _ = self.start_line
        _ = self.stop_line
        assert self.tree_attributes.script_context.script[: self.start_position].count("\n") == self.start_line
        try:
            assert (
                self.tree_attributes.script_context.script[max(0, self.start_position - 1) :: -1].index("\n")
                == self.start_column
            )
        except ValueError:
            assert self.start_position == self.start_column

        assert self.tree_attributes.script_context.script[: self.stop_position].count("\n") == self.stop_line
        try:
            assert (
                self.tree_attributes.script_context.script[max(0, self.stop_position - 1) :: -1].index("\n") == self.stop_column
            )
        except ValueError:
            assert self.start_position == self.start_column

    def check_init(self) -> None:  # noqa: D102
        super().check_init()
        self._check_positions()

    def pretty_line(self, replaced_content: str, content_size: int) -> str:  # noqa: D102
        NNEWLINE = "\n"  # noqa: N806 pylint: disable=invalid-name
        DOUBLE_SLASH_N = "\\n"  # noqa: N806 pylint: disable=invalid-name
        return (
            f"column {self.start_column if self.start_column is not None else '???':3} "
            f"from {self.start_position if self.start_position is not None else '?????':5} :   "
            f"{replaced_content.replace(NNEWLINE, DOUBLE_SLASH_N)[:content_size]:{content_size}}   -> "
            f"{self.stop_position if self.stop_position is not None else '?????':5}"
        )

    @staticmethod
    def duck_copy(
        root_or_subroot: Tree[TerminalType, RuleType, TreeDataType, NodeDataType],
        *,
        deep_copy_node_data: bool = False,
    ) -> ClassicTree[TerminalType, RuleType, TreeDataType, NodeDataType, TokenDataType_co]:
        """Construct a ClassicTree based tree from a Tree (or subclass) based tree.

        There are no check that the tokens have line and column attribute.
        """
        return cast(ClassicTree[TerminalType, RuleType, TreeDataType, NodeDataType, TokenDataType_co], duck_copy(
            self=root_or_subroot,
            deep_copy_node_data=deep_copy_node_data,
            cls=ClassicTree,
        ))

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
    )
