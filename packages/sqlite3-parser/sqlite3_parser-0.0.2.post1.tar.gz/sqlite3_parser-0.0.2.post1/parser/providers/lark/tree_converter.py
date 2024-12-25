"""Implement custom lexer to be used by lark parser and convert Lark ParseTree into tree.Tree."""
# ruff: noqa: SLF001

from __future__ import annotations

from collections.abc import Generator, Iterable
from enum import Enum
from typing import Any, Self, cast

from lark import Lark, ParseTree
from lark import Token as LarkToken
from lark import Tree as LarkTree
from lark.lexer import Lexer, LexerState  # type: ignore

from parser.script_context import ScriptContext
from parser.tree.classic_tree import ClassicTree
from parser.tree.protocols import ClassicalTokenProtocol
from parser.tree.tree import Tree, TreeAttributes


class _TreeWithLarkNode[
    TerminalType: Enum,
    RuleType: Enum,
    TreeDataType,
    NodeDataType,
    TokenDataType,
](Tree[TerminalType, RuleType, TreeDataType, NodeDataType]):  # pylint: disable=W0223
    """Tree with matching Lark ParseTree node or Lark token bound at each Tree node."""

    lark_node: (
        LarkTree[LarkTokenWithOriginalNode[TerminalType, TokenDataType]]
        | LarkTokenWithOriginalNode[TerminalType, TokenDataType]
        | None
    ) = None

    __setattr__ = object.__setattr__  # type: ignore


def _build_attached_tree[
    TerminalType: Enum,
    RulesType: Enum,
    TokenDataType,
](
    input_tree: ParseTree,
    script_context: ScriptContext[TerminalType],
) -> _TreeWithLarkNode[TerminalType, RulesType, None, None, TokenDataType]:  # pyright: ignore[reportInvalidTypeVarUse]
    """Build tree with matching lark node linked in lark_node and link children to parents."""
    input_tree_ = cast(LarkTree[LarkTokenWithOriginalNode[TerminalType, TokenDataType]], input_tree)
    root_tree_attributes: TreeAttributes[TerminalType, None] = TreeAttributes(script_context)
    root: _TreeWithLarkNode[TerminalType, RulesType, None, None, TokenDataType] = _TreeWithLarkNode(
        tree_attributes=root_tree_attributes,
    )
    root.lark_node = input_tree_
    current: list[_TreeWithLarkNode[TerminalType, RulesType, None, None, TokenDataType]] = [root]
    next_ones: list[_TreeWithLarkNode[TerminalType, RulesType, None, None, TokenDataType]] = []

    while current:
        for element in current:
            if isinstance(element.lark_node, LarkTree):
                for lark_child in element.lark_node.children:
                    child: _TreeWithLarkNode[TerminalType, RulesType, None, None, TokenDataType] = _TreeWithLarkNode(
                        root_tree_attributes,
                    )
                    child.lark_node = lark_child
                    next_ones.append(child)
                    element.add_children(child)
        current = next_ones
        next_ones = []
    root._parent = None
    return root


def _transfer_node_content[
    TerminalType: Enum,
    RulesType: Enum,
    TreeDataType,
    NodeDataType,
    TokenDataType,
](
    tree: _TreeWithLarkNode[TerminalType, RulesType, TreeDataType, NodeDataType, TokenDataType],
    rules_enum: type[RulesType],
) -> None:
    for node in tree:
        source: (
            LarkTree[LarkTokenWithOriginalNode[TerminalType, TokenDataType]]
            | LarkTokenWithOriginalNode[TerminalType, TokenDataType]
            | None
        ) = node.lark_node

        if isinstance(source, LarkTokenWithOriginalNode):
            assert not node.children
            node._token = source.original_token
            token_count = tree.tree_attributes.script_context.active_token_to_index[node._token]
            node._active_tokens_bounds = slice(token_count, token_count + 1)
            node._rule = None

        elif isinstance(source, LarkTree):
            assert cast(LarkToken, source.data).type == "RULE"
            node._rule = rules_enum(source.data)
            node._token = None
        else:
            node._token = None
            node._rule = None


def convert_lark_tree_to_tree[
    TerminalType: Enum,
    RulesType: Enum,
    TreeDataType,
    NodeDataType,
    TokenDataType,
](
    input_tree: ParseTree,
    script_context: ScriptContext[TerminalType],
    rules_enum: type[RulesType],
    *,
    attach_index: int = 0,
) -> Tree[TerminalType, RulesType, None, None]:  # pyright: ignore[reportInvalidTypeVarUse]
    """Produce an equivalent tree.Tree using a Lark ParseTree.

    Leftover can be retrieved using content bounds.
    """
    root: _TreeWithLarkNode[TerminalType, RulesType, None, None, TokenDataType] = _build_attached_tree(
        input_tree,
        script_context,
    )

    _transfer_node_content(root, rules_enum)

    root.update_from_leaves(attach_index=attach_index)

    ret: Tree[TerminalType, RulesType, None, None] = root.get_detached_subtree_copy(attach_index=attach_index)

    _ = ret.check()
    ret.tree_attributes.state.checked = False
    ret.reload()

    return ret


class LarkTokenWithOriginalNode[TerminalType: Enum, TokenDataType](LarkToken):
    """Lark token with an original_token slot for a Token."""

    __slots__ = ("original_token",)
    original_token: ClassicalTokenProtocol[TerminalType, TokenDataType]

    def __new__(cls, original_token: ClassicalTokenProtocol[TerminalType, TokenDataType], *args: Any, **kwargs: Any) -> Self:  # noqa: ANN401
        ret = cast(Self, super().__new__(cls, *args, **kwargs))
        ret.original_token = original_token
        return ret


class PassThroughLexer[TerminalType: Enum, TokenDataType](Lexer):
    """When this lexer is used, just pass the parsed token list to parse function in place of a string."""

    def __init__(self, lexer_conf: object) -> None:
        del lexer_conf
        super().__init__()

    def lex(
        self,
        lexer_state: LexerState | str | Iterable[ClassicalTokenProtocol[TerminalType, TokenDataType]],
        parser_state: object = None,
    ) -> Generator[LarkTokenWithOriginalNode[TerminalType, TokenDataType], None, None]:
        """Bind Token to SQLiteLexerToken and yield them."""
        del parser_state
        for token in cast(Iterable[ClassicalTokenProtocol[TerminalType, TokenDataType]], lexer_state):
            yield LarkTokenWithOriginalNode(
                original_token=token,
                type=token.token_type.value,
                value=token.content,
                start_pos=token.start_position,
                end_pos=token.start_position + len(token.content),
                column=token.start_column,
                end_column=token.stop_column,
                line=token.start_line,
                end_line=token.stop_line,
            )


class LarkParser[TerminalType: Enum, RulesType: Enum]:
    """Create a parser from a given Lark grammar, then use it to parse a list of tokens."""

    def __init__(
        self,
        grammar: str,
        rules_enum: type[RulesType],
    ) -> None:
        """Create the lark.Lark object with the given grammar and PassThroughLexer."""
        self.parser = Lark(grammar=grammar, parser="earley", lexer=PassThroughLexer)
        self.rules_enum = rules_enum

    def parse[TokenDataType](
        self,
        active_tokens_list: Iterable[ClassicalTokenProtocol[TerminalType, TokenDataType]],
        script_context: ScriptContext[TerminalType],
        active_token_chunk_bounds: slice,
        *,
        deep_copy_node_data: bool = False,
    ) -> ClassicTree[TerminalType, RulesType, None, None, TokenDataType]:
        """Parse the given token list (not str).

        active_tokens_list is passed just to infer eventual data existance.
        """
        assert not active_tokens_list or all(
            a == b and type(a) is type(b)
            for a, b in zip(
                active_tokens_list,
                script_context.active_token_list,
                strict=True,
            )
        )
        del active_tokens_list
        _active_tokens_list: str = cast(str, script_context.active_token_list)
        parsed = self.parser.parse(_active_tokens_list[active_token_chunk_bounds])
        tree = convert_lark_tree_to_tree(
            parsed,
            script_context,
            self.rules_enum,
            attach_index=active_token_chunk_bounds.start,
        )
        return ClassicTree[TerminalType, RulesType, None, None, TokenDataType].duck_copy(
            root_or_subroot=tree,
            deep_copy_node_data=deep_copy_node_data,
        )


__all__ = [
    "LarkParser",
]
