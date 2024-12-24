"""Implements the Tree class which is root, nodes and leaf of the Tree it consist."""

from __future__ import annotations

from collections.abc import Callable, Generator, Iterator
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from functools import cache, cached_property
from itertools import pairwise
from re import Pattern, match, search
from typing import Any, Literal, Self, cast, overload

from .protocols import TokenProtocol
from .tree_auxiliary import (
    ContentMatch,
    DynamicMatchAttributeHelper,
    MatchItem,
    Singleton,
    TreeAttributes,
    UninitializedError,
    _TreeSate,
)

MAX_CHILDS_AS_ATTRIBUTE = 30
SMALLEST_REGEX_STR_LEN = len("//")


class _NotSetType(Singleton):
    pass


_NotSet = _NotSetType()


class _NotSetUnpickledTokenType(Singleton):
    pass


_NotSetUnpickledToken = _NotSetUnpickledTokenType()


def duck_copy[
    TreeType: Tree,  # type: ignore
    TerminalType: Enum,
    RuleType: Enum,
    TreeDataType,
    NodeDataType,
](
    self: Tree[TerminalType, RuleType, TreeDataType, NodeDataType],
    cls: type[TreeType],
    *,
    deep_copy_node_data: bool = False,
    top_caller: bool = True,
) -> TreeType:
    """Try to construct a cls based tree from a Tree (or subclass) tree."""
    if top_caller:
        initial_state: _TreeSate = self.tree_attributes.state
    self.tree_attributes.state.locked = False
    self.tree_attributes.state.building = True
    tree: TreeType = cls(
        self.tree_attributes,
        self.token,
        self.rule,
        [],
        None,
        self.active_tokens_bounds,
        deepcopy(self.node_data) if deep_copy_node_data else self.node_data,
    )
    new_childs: Generator[TreeType] = (
        duck_copy(
            child,
            top_caller=False,
            cls=cls,
        )
        for child in self.children
    )
    tree.add_children(*new_childs)  # type: ignore
    if top_caller:
        self.tree_attributes.state = initial_state  # pyright: ignore[reportPossiblyUnboundVariable]
    return tree


class Tree[TerminalType: Enum, RulesType: Enum, TreeDataType, NodeDataType]:
    r"""Implement the building block of a tree (a node), that can either be a rule or a token.

    If you use regex matching, be sure to know :
    * the difference between search, match, and fullmatch
    * whether . matches \n
    * that you need to wrap your str bewteen two / forward slash or it will be compared litterally.
    """

    @property
    def _building_attributes(self) -> set[str]:
        return {
            "tree_attributes",
            "_token",
            "_rule",
            "children",
            "_parent",
            "_active_tokens_bounds",
        }

    def __init__(  # noqa: PLR0913
        self,
        tree_attributes: TreeAttributes[TerminalType, TreeDataType],
        token: TokenProtocol[TerminalType] | None | _NotSetType = _NotSet,
        rule: RulesType | None | _NotSetType = _NotSet,
        children: list[Self] | None = None,
        parent: Self | None | _NotSetType = _NotSet,
        active_tokens_bounds: slice | _NotSetType = _NotSet,
        node_data: NodeDataType | None = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        """tree_attributes contains everything that is shared at the tree-level."""
        super().__init__(**kwargs)

        self.tree_attributes: TreeAttributes[TerminalType, TreeDataType]
        object.__setattr__(self, "tree_attributes", tree_attributes)

        self._token: TokenProtocol[TerminalType] | None | _NotSetType = token
        self._rule: RulesType | None | _NotSetType = rule
        self._active_tokens_bounds: slice | _NotSetType = active_tokens_bounds

        self.children: list[Self]
        if children is not None:
            self.children = children
        else:
            self.children = cast(list[Self], [])
        self._parent: Self | None | _NotSetType = parent

        self.node_data: NodeDataType | None = node_data

    ##############################################################################################################
    ##############################################################################################################

    def __hash__(self) -> int:
        """Hash entire tree, and the path from the root to the node."""
        return hash((self.root.tree_attributes, self.root._reduce(), *self.path))

    def _retrieve_script_context_token(self) -> None:
        assert self.root is self

        def override_token(node: Tree[TerminalType, RulesType, TreeDataType, NodeDataType]) -> None:
            if node._token is not None:
                assert node.active_tokens_bounds.stop - node.active_tokens_bounds.start == 1
                object.__setattr__(node, "token", node.active_token_content[0])
                object.__setattr__(node, "_token", node.active_token_content[0])

        self.process_tree_bottom_up(override_token)

    def _check_script_context_token(self) -> Literal[True]:
        assert self.root is self

        def override_token(node: Tree[TerminalType, RulesType, TreeDataType, NodeDataType]) -> None:
            if node._token is not None:
                assert node.active_token_content[0] == node._token
                assert node.active_tokens_bounds.stop - node.active_tokens_bounds.start == 1

        self.process_tree_bottom_up(override_token)
        return True

    def get_detached_subtree_copy(
        self,
        *,
        attach_index: int = 0,
    ) -> Tree[TerminalType, RulesType, TreeDataType, NodeDataType]:
        """Get a standalone tree deep copied from the subtree rooted on this node."""
        factory, content = cast(Any, deepcopy(self.__reduce__()))
        return factory(*content, attach_index=attach_index)

    def _set_active_bound_start_to(self, reference_active_tokens_bounds: int) -> None:
        assert self.root is self
        offset = reference_active_tokens_bounds - self.active_tokens_bounds.start
        for node in self:
            if not node._token is not None:
                continue
            orig = node.active_tokens_bounds
            orig = slice(orig.start + offset, orig.stop + offset)
            del node.active_tokens_bounds
            node._active_tokens_bounds = orig

    @staticmethod
    def _unreduce(
        tree_attributes: TreeAttributes[TerminalType, TreeDataType],
        pickling_tree: PicklingTree[TerminalType, RulesType, NodeDataType],
        parent: Tree[TerminalType, RulesType, TreeDataType, NodeDataType] | None = None,
        *,
        attach_index: int = 0,
    ) -> Tree[TerminalType, RulesType, TreeDataType, NodeDataType]:
        ret = Tree(
            tree_attributes=tree_attributes,
            children=[],
            active_tokens_bounds=pickling_tree.active_tokens_bounds,
            node_data=pickling_tree.node_data,
            parent=parent,
            token=pickling_tree.token,
            rule=pickling_tree.rule,
        )
        ret.add_children(
            *[
                cast(Tree[TerminalType, RulesType, TreeDataType, NodeDataType], Tree)._unreduce(tree_attributes, pt, ret)
                for pt in pickling_tree.children
            ],
        )
        if parent is None:
            ret.update_from_leaves(attach_index=attach_index)
        return ret

    def _reduce(
        self,
    ) -> PicklingTree[TerminalType, RulesType, NodeDataType]:
        return PicklingTree(
            self.token,
            self.rule,
            [child._reduce() for child in self.children],
            self.active_tokens_bounds if self.token is not None else _NotSet,
            self.node_data,
        )

    def __reduce__(self) -> tuple[
        Callable[[
            TreeAttributes[TerminalType, TreeDataType],
            PicklingTree[TerminalType, RulesType, NodeDataType],
        ], Tree[TerminalType, RulesType, TreeDataType, NodeDataType]],
        tuple[TreeAttributes[TerminalType, TreeDataType], PicklingTree[TerminalType, RulesType, NodeDataType]],
    ]:
        """NodeDataType and TreeDataType must be picklable type."""
        return (
            self._unreduce,
            (
                self.tree_attributes,
                self._reduce(),
            ),
        )

    def __deepcopy__(self, memo: object) -> Tree[TerminalType, RulesType, TreeDataType, NodeDataType]:
        """Deep copy the whole tree, and get returns the node at the same position in the tree than this one."""
        path: list[int] = deepcopy(self.path)
        factory, content = deepcopy(self.root.__reduce__())
        return (factory(*content))[path]

    ##############################################################################################################
    ##############################################################################################################

    @cached_property
    def token(self) -> TokenProtocol[TerminalType] | None:
        """Proxy checking that the value has been initialized before use."""
        if self._token is _NotSet:
            raise UninitializedError
        ret = self._token
        return cast(TokenProtocol[TerminalType] | None, ret)

    @cached_property
    def rule(self) -> RulesType | None:
        """Proxy checking that the value has been initialized before use."""
        if self._rule is _NotSet:
            raise UninitializedError
        ret = self._rule
        return cast(RulesType | None, ret)

    @cached_property
    def parent(self) -> Self | None:
        """Proxy checking that the value has been initialized before use."""
        if self._parent is _NotSet:
            raise UninitializedError
        ret = self._parent
        return cast(Self | None, ret)

    @cached_property
    def active_tokens_bounds(self) -> slice:
        """Proxy checking that the value has been initialized before use."""
        if self._active_tokens_bounds is _NotSet:
            raise UninitializedError
        ret = self._active_tokens_bounds
        return cast(slice, ret)

    ##############################################################################################################
    ##############################################################################################################

    def _ep_equal_bounds(self) -> tuple[TokenProtocol[TerminalType], Literal["left", "right"]] | Literal[0]:
        pep = cast(Self, self.parent).enclosing_token_pair
        match pep:
            case 0 | tuple([_, "left" | "right"]):
                patkb = cast(Self, self.parent).active_tokens_bounds
                assert patkb.start == patkb.stop
                return pep
            case tuple():
                pch: list[Self] = cast(Self, self.parent).children
                pos: int = [id(child) for child in pch].index(id(self))
                if self.active_tokens_bounds.start != cast(Self, self.parent).active_tokens_bounds.start:
                    match pch[pos - 1].enclosing_token_pair:
                        case tuple([_, "left" | "right" as must_be_right]) as ret:
                            assert must_be_right == "right"
                            return ret
                        case tuple([_, right]):
                            return right, "right"
                        case _:  # pragma: no cover
                            raise RuntimeError
                match pch[pos + 1].enclosing_token_pair:
                    case tuple([_, "left" | "right" as must_be_left]) as ret:
                        assert must_be_left == "left"
                        return ret
                    case tuple([left, _]):
                        return left, "left"
                    case _:  # pragma: no cover
                        raise RuntimeError
            case _:  # pragma: no cover
                raise RuntimeError

    @cached_property
    def enclosing_token_pair(
        self,
    ) -> (
        tuple[TokenProtocol[TerminalType], TokenProtocol[TerminalType]]
        | tuple[TokenProtocol[TerminalType], Literal["left", "right"]]
        | Literal[0]
    ):
        """Return the first and last active token of this Tree (that can be the same).

        If the tree doesn't have any, return a tuple containing two None and the previous Token.
        If there is no previous token, and the tree is empty, return (None, None, 0).
        """
        assert isinstance(self.active_tokens_bounds, slice)
        assert isinstance(self.active_tokens_bounds.start, int)
        assert isinstance(self.active_tokens_bounds.stop, int)
        if self.active_tokens_bounds.start < self.active_tokens_bounds.stop:
            return (
                self.tree_attributes.script_context.active_token_list[self.active_tokens_bounds.start],
                self.tree_attributes.script_context.active_token_list[self.active_tokens_bounds.stop - 1],
            )
        elif self.active_tokens_bounds.start > self.active_tokens_bounds.stop:
            raise AssertionError
        elif self.parent is None:
            if self.tree_attributes.script_context.active_token_list:
                if self.active_tokens_bounds.start != 0:
                    return (
                        self.tree_attributes.script_context.active_token_list[self.active_tokens_bounds.start - 1],
                        "right",
                    )
                else:
                    return self.tree_attributes.script_context.active_token_list[self.active_tokens_bounds.start], "left"
            return 0
        else:
            return self._ep_equal_bounds()

    @cached_property
    def content_bounds(self) -> slice:
        """Get the bounds of this tree in the input text."""
        ep = self.enclosing_token_pair
        match ep:
            case tuple([token, "left"]):
                p = cast(TokenProtocol[TerminalType], token).start_position  # pyright: ignore[reportUnnecessaryCast]
                return slice(p, p)
            case tuple([token, "right"]):
                p = cast(TokenProtocol[TerminalType], token).stop_position  # pyright: ignore[reportUnnecessaryCast]
                return slice(p, p)
            case tuple():
                start_token, stop_token = ep
                assert not isinstance(stop_token, str)
                return slice(start_token.start_position, stop_token.stop_position)
            case 0:
                return slice(0, 0)
            case _:  # pragma: no cover
                raise RuntimeError

    @cached_property
    def tokens_bounds(self) -> slice:
        """Get the bounds of this tree in the full token list."""
        match self.enclosing_token_pair:
            case 0:
                return slice(0, 0)
            case tuple([bound, "left" | "right" as side]):
                i = self.tree_attributes.script_context.token_to_index[bound]
                if side == "left":
                    return slice(i, i)
                i += 1
                return slice(i, i)
            case tuple([left, right]):
                tti = self.tree_attributes.script_context.token_to_index
                return slice(
                    tti[left],
                    tti[right] + 1,
                )
            case _:  # pragma: no cover
                raise RuntimeError

    @cached_property
    def start_position(self) -> int:
        """Get the start position of this tree in the input text."""
        return self.content_bounds.start

    @cached_property
    def stop_position(self) -> int:
        """Get the stop position of this tree in the input text."""
        return self.content_bounds.stop

    def __len__(self) -> int:
        """Get the length of the contained string, including ignored text as long as it is not at a boundary."""
        return self.content_length

    @cached_property
    def content_length(self) -> int:
        """Get the length of the contained string, including ignored text as long as it is not at a boundary."""
        assert self.content_bounds.step in [None, 1]
        return self.content_bounds.stop - self.content_bounds.start

    @cached_property
    def content(self) -> str:
        """The text enclosed between active Tokens participating to this rule, or the text matched by this token."""
        assert self.content_bounds.step in [None, 1]
        return self.tree_attributes.script_context.script[self.content_bounds]

    @cached_property
    def token_length(self) -> int:
        """Total number of token in this Tree, active or not."""
        assert self.tokens_bounds.step in [None, 1]
        return self.tokens_bounds.stop - self.tokens_bounds.start

    @cached_property
    def token_content(self) -> tuple[TokenProtocol[TerminalType], ...]:
        """Tokens, active or not, that are part of this tree."""
        assert self.tokens_bounds.step in [None, 1]
        return tuple(self.tree_attributes.script_context.token_list[self.tokens_bounds])

    @cached_property
    def active_token_length(self) -> int:
        """Total number of active token in this Tree."""
        assert self.active_tokens_bounds.step in [None, 1]
        return self.active_tokens_bounds.stop - self.active_tokens_bounds.start

    @cached_property
    def active_token_content(
        self,
    ) -> tuple[TokenProtocol[TerminalType], ...]:
        """Active tokens that are part of this tree."""
        assert self.active_tokens_bounds.step in [None, 1]
        return tuple(self.tree_attributes.script_context.active_token_list[self.active_tokens_bounds])

    @cached_property
    def is_no_match(self) -> bool:
        """The rules made optionnal with a pair of [brackets] leaves a None in the tree when they do not match.

        Return true if this Tree node is such optional that didn't match.
        """
        return self.token is None and self.rule is None

    @cached_property
    def is_token(self) -> bool:
        """Return true if this Tree node is a Token."""
        return self.token is not None

    @cached_property
    def is_rule(self) -> bool:
        """Return true if this Tree node is a rule."""
        return self.rule is not None

    @cached_property
    def element(self) -> TerminalType | RulesType | None:
        """Return the type of the current node (Tree) : TokenType, RulesTypes or None."""
        if self.is_rule:
            assert not self.is_token
            return self.rule
        elif self.is_token:
            assert self.token is not None
            return self.token.token_type
        else:
            return None

    @cached_property
    def path(self) -> list[int]:
        """Position in the child of each ancestor to reach the node, starting from the root."""
        return [[id(c) for c in parent.children].index(id(child)) for child, parent in pairwise([self, *self.ancestors])][::-1]

    @cached_property
    # def root(self) -> Self:
    def root(self) -> Tree[TerminalType, RulesType, TreeDataType, NodeDataType]:
        """Root of the tree of which this node is part."""
        return self.ancestors[-1] if self.ancestors else self

    ##############################################################################################################
    ##############################################################################################################

    @cached_property
    def fullmatch_content(self) -> ContentMatch[TerminalType, RulesType, TreeDataType, NodeDataType]:
        """Use re.fullmatch."""
        assert self.content is not None
        return ContentMatch(self.content, self)

    @cached_property
    def case_sensitive_fullmatch_content(self) -> ContentMatch[TerminalType, RulesType, TreeDataType, NodeDataType]:
        """Use re.fullmatch."""
        assert self.content is not None
        return ContentMatch(self.content, self, case_sensitive=True)

    @cached_property
    def regexable_content(self) -> ContentMatch[TerminalType, RulesType, TreeDataType, NodeDataType]:
        """Use re.fullmatch."""
        assert self.content is not None
        return ContentMatch(self.content, self)

    @cached_property
    def case_sensitive_regexable_content(self) -> ContentMatch[TerminalType, RulesType, TreeDataType, NodeDataType]:
        """Use re.fullmatch."""
        assert self.content is not None
        return ContentMatch(self.content, self, case_sensitive=True)

    @cached_property
    def match_content(self) -> ContentMatch[TerminalType, RulesType, TreeDataType, NodeDataType]:
        """Use re.match."""
        assert self.content is not None
        return ContentMatch(self.content, self, regex_function=match)

    @cached_property
    def case_sensitive_match_content(self) -> ContentMatch[TerminalType, RulesType, TreeDataType, NodeDataType]:
        """Use re.match."""
        assert self.content is not None
        return ContentMatch(self.content, self, case_sensitive=True, regex_function=match)

    @cached_property
    def search_content(self) -> ContentMatch[TerminalType, RulesType, TreeDataType, NodeDataType]:
        """Use re.search."""
        assert self.content is not None
        return ContentMatch(self.content, self, regex_function=search)

    @cached_property
    def case_sensitive_search_content(self) -> ContentMatch[TerminalType, RulesType, TreeDataType, NodeDataType]:
        """Use re.search."""
        assert self.content is not None
        return ContentMatch(self.content, self, case_sensitive=True, regex_function=search)

    ##############################################################################################################
    ##############################################################################################################

    def _list_depth_first_with_levels(
        self,
        level: int = 0,
    ) -> list[tuple[Self, int]]:
    # ) -> list[tuple[Tree[TerminalType, RulesType, TreeDataType, NodeDataType], int]]:
        """Yield the node and its nesting level, then its first child and its nesting level (n + 1), \

        then its first child, and then goes to the deepest next child.
        """
        ret: list[tuple[Self, int]] = []
        ret.append((self, level))
        for child in self.children:
            ret.extend(child._list_depth_first_with_levels(level + 1))
        return ret

    @cached_property
    def depth_first_list_with_nexting_levels(self) -> list[tuple[Self, int]]:
        """List all nodes depth first as tuples with their respective nesting levels."""
        return self._list_depth_first_with_levels()

    @cached_property
    def total_childs_number(self) -> int:
        """Recursively get the total child number, including self."""
        return 1 + sum(c.total_childs_number for c in self.children)

    @cached_property
    def breadthfirst_list(self) -> list[Self]:
        """Return all the children from each depth level starting at the root, starting at the left every time."""
        ret: list[Self] = []
        current: list[Self] = [self]
        next_ones: list[Self] = []
        while current:
            for element in current:
                ret.append(element)
                next_ones.extend(element.children)
            current = next_ones
            next_ones = []
        return ret

    @cached_property
    def bottom_to_top_right_to_left_list(self) -> list[Self]:
        """Return all the children from each depth level ending at the root, starting at the left every time."""
        return list(reversed(list(self.breadthfirst_list)))

    @cached_property
    def depth_first_right_to_left_list(self) -> list[Self]:
        """Yield the node, then its last child, then its last child, and then goes to the deepest next child."""
        ret: list[Self] = []
        ret.append(self)
        for child in reversed(self.children):
            ret.extend(child.depth_first_right_to_left_list)
        return ret

    @cached_property
    def depth_first_list(self) -> list[Self]:
        """Yield the node, then its first child, then its first child, and then goes to the deepest next child."""
        ret: list[Self] = []
        ret.append(self)
        for child in self.children:
            ret.extend(child.depth_first_list)
        return ret

    def __iter__(self) -> Iterator[Self]:
        """Yield the node, then its first child, then its first child, and then goes to the deepest next child."""
        return iter(self.depth_first_list)

    @cached_property
    def repr(self) -> str:
        """Start and stop position, and rule name or TokenType are aligned. Also dislay the first four children."""
        if self.rule is None and self.token is None:
            content: Any = "[None]"
        elif self.token is not None:
            content = self.token.token_type.name
        elif self.rule is not None:
            content = self.rule.name
        else:
            raise AssertionError

        return f"""{self.start_position:5} {content:20} {self.stop_position:5}"""

    def __repr__(self) -> str:  # noqa: D105
        return self.repr

    @cached_property
    # def ancestors(self) -> list[Self]:
    def ancestors(self) -> list[Tree[TerminalType, RulesType, TreeDataType, NodeDataType]]:
        """Return the list of all the ancestor.

        Exclude the node on which this function was called, start with the direct parent and finish with the root.
        """
        ancestors: list[Tree[TerminalType, RulesType, TreeDataType, NodeDataType]] = []
        current: Self = self
        while current.parent is not None:
            current = current.parent
            ancestors.append(current)
        return ancestors

    @cached_property
    def is_leaf(self) -> bool:
        """Return whether the node doesn't have any children."""
        return not self.children

    @cached_property
    def ancestor_rules_types(self) -> set[RulesType]:
        """Set containing every different RulesTypes present in (direct and indirect) ancestors."""
        assert all(isinstance(ancestor.rule, Enum) for ancestor in self.ancestors)
        return {cast(RulesType, ancestor.rule) for ancestor in self.ancestors}

    @cached_property
    def descendants_elements(self) -> set[None | RulesType | TerminalType]:
        """Set containing every different element present in (direct and indirect) descendants."""
        return {node.element for node in self}

    @cached_property
    def has_unordered_ancestors_rulestypes(self) -> DynamicMatchAttributeHelper:
        """Equal to value if the given RulesTarget exists in the order provided in ancestors.

        Possibly skipping ancestors but using the order provided.
        """

        def _condition(value: object) -> bool:
            if isinstance(value, Enum):
                return value in self.ancestor_rules_types
            return False

        return DynamicMatchAttributeHelper(_condition)

    @cached_property
    def has_unordered_elements_in_descendants(self) -> DynamicMatchAttributeHelper:
        """Match if element is present in descendant."""

        def _condition(value: object) -> bool:
            if not isinstance(value, (None | Enum)):
                return False
            element: None | RulesType | TerminalType = cast(None | RulesType | TerminalType, value)  # pyright: ignore[reportUnnecessaryCast]
            return element in self.descendants_elements

        return DynamicMatchAttributeHelper(_condition)

    @cached_property
    def ignored_token_content(self) -> tuple[TokenProtocol[TerminalType], ...]:
        """List every ignored token in the subtree, as long as they are (immediately or not) between active tokens."""
        return tuple(
            token
            for token in self.token_content
            if token.token_type in self.tree_attributes.script_context.ignored_tokens_types
        )

    @cached_property
    def ignored_content(self) -> str:
        """Merged contained whitespaces, not only comments."""
        return "".join(token.content for token in self.ignored_token_content)

    @cached_property
    def left_ignored_token(self) -> tuple[TokenProtocol[TerminalType], ...]:
        """Ignored tokens preceding the subtree, until the first active token."""
        left: list[TokenProtocol[TerminalType]] = []
        for token in self.tree_attributes.script_context.token_list[: self.tokens_bounds.start][::-1]:
            if token.token_type not in self.tree_attributes.script_context.ignored_tokens_types:
                break
            left.append(token)
        return tuple(reversed(left))

    @cached_property
    def left_greedy_ignored_content(self) -> str:
        """Merged contained whitespaces and all preceding whitespaces until next active token, not only comments."""
        return "".join(token.content for token in self.left_ignored_token) + self.ignored_content

    @cached_property
    def regexable_ignored_content(
        self,
    ) -> ContentMatch[TerminalType, RulesType, TreeDataType, NodeDataType]:
        """Match the provided regex or str against left_greedy_whitespace_content."""
        return ContentMatch(
            self.left_greedy_ignored_content,
            self,
            case_sensitive=True,
            regex_function=search,
        )

    @cached_property
    def match_total_children_number(self) -> DynamicMatchAttributeHelper:
        """Match against (min, max) or exact_value."""

        def _content(value: object) -> bool:
            match value:
                case tuple(["max", int(max_)]):
                    return self.total_childs_number <= max_
                case tuple(["min", int(min_)]):
                    return min_ <= self.total_childs_number
                case int():
                    return self.total_childs_number == value
            raise TypeError

        return DynamicMatchAttributeHelper(_content)

    @cached_property
    def match_direct_children_number(self) -> DynamicMatchAttributeHelper:
        """Match against (min, max) or exact_value."""

        def _content(value: object) -> bool:
            match value:
                case tuple(["max", int(max_)]):
                    return len(self.children) <= max_
                case tuple(["min", int(min_)]):
                    return min_ <= len(self.children)
                case int():
                    return len(self.children) == value
            raise TypeError

        return DynamicMatchAttributeHelper(_content)

    @cached_property
    def active_content(self) -> str:
        """Contents of all descendant active token in order, join using the specified str."""
        return self.tree_attributes.active_token_remerge_character.join(token.content for token in self.active_token_content)

    @cached_property
    def match_active_content(
        self,
    ) -> ContentMatch[TerminalType, RulesType, TreeDataType, NodeDataType]:
        """Merged by a space."""
        return ContentMatch(
            self.active_content,
            self,
            regex_function=search,
        )

    @cached_property
    def lines(self) -> DynamicMatchAttributeHelper:  # actually positions if not overriden.
        """Docstring possibly outdated.

        Match if the given line contains part of node's content, or is adjacent to a newline part of the node's content.

        If two positions are given, the startline and endline should be exactly these two numbers.

        If there is no columns and lines coordinates, fallback on positions.
        The difference is that if it is a tuple (not a slice), \
            the content should be between caracters at the indexes (but doesn't have to up to those bounds).
        """

        def _condition(value: object) -> bool:
            match value:
                case int():
                    return self.start_position <= value <= self.stop_position
                case tuple(["max", int(max_)]):
                    return self.stop_position >= max_
                case tuple(["min", int(min_)]):
                    return self.start_position <= min_
            raise TypeError

        return DynamicMatchAttributeHelper(_condition)

    ##############################################################################################################
    ##############################################################################################################

    def _discard_cache(self) -> None:
        poplist: list[str] = []
        for name in self.__dict__:
            if isinstance(
                getattr(
                    self.__class__,
                    name,
                    None,
                ),
                cached_property,
            ):
                poplist.append(name)  # noqa: PERF401
        for name in poplist:
            object.__delattr__(self, name)

    ##############################################################################################################
    ##############################################################################################################

    @staticmethod
    def _enum_compare(a: Enum | None, b: Enum | None) -> bool:
        if type(a) is type(b) or not isinstance(a, int) or not isinstance(b, int):
            return a == b
        return False

    @overload  # type: ignore
    def __eq__(
        self,
        value: Self,
    ) -> bool:
        raise NotImplementedError

    @overload  # type: ignore
    def __eq__(
        self,
        value: Tree[Enum, Enum, Any, Any],
    ) -> bool:
        raise NotImplementedError

    @overload
    def __eq__(
        self,
        value: Enum | None,
    ) -> bool:
        raise NotImplementedError

    @overload  # type: ignore
    def __eq__(
        self,
        value: Pattern[str],
    ) -> list[MatchItem[TerminalType, RulesType, TreeDataType, NodeDataType]]:
        raise NotImplementedError

    @overload  # type: ignore
    def __eq__(
        self,
        value: str,
    ) -> bool | list[MatchItem[TerminalType, RulesType, TreeDataType, NodeDataType]]:
        raise NotImplementedError

    @overload  # type: ignore
    def __eq__(
        self,
        value: object,
    ) -> bool | list[MatchItem[TerminalType, RulesType, TreeDataType, NodeDataType]]:
        raise NotImplementedError

    def __eq__(  # type: ignore
        self,
        value: object,
    ) -> bool | list[MatchItem[TerminalType, RulesType, TreeDataType, NodeDataType]]:
        """Compare two subtrees and return true if they have (probably) identical semantical roles, and the same content.

        For instance, a statement subtrees from a programming language should compare equal to itself regardless
            of its neighbours and position among the parent syntax element (unless this element was changed).
        """
        if self is value:
            return True
        match value:
            case Tree():
                return (
                    self.compare_trees_and_nodes_positions(cast(Tree[Enum, Enum, Any, Any], value))
                    if self.tree_attributes.strict_comparison
                    else (
                        self._ancestors_compare(cast(Tree[Enum, Enum, Any, Any], value))
                        and self.compare_subtrees(cast(Tree[Enum, Enum, Any, Any], value))
                    )
                )
            case None | Enum():
                return self._enum_compare(self.element, value)
            case Pattern() if isinstance(cast(Pattern[bytes] | Pattern[str], value).pattern, bytes):
                return NotImplemented
            case str() | Pattern():
                return ContentMatch(
                    self.content,
                    self,
                ).get_matches_against(cast(Pattern[str], value))
            case _:
                return NotImplemented

    def _ancestors_compare(
        self,
        other: Tree[Enum, Enum, Any, Any],
    ) -> bool:
        try:
            assert all(sa.is_rule and oa.is_rule for sa, oa in zip(self.ancestors, other.ancestors, strict=True))
            return all(
                self._enum_compare(sa.element, oa.element) for sa, oa in zip(self.ancestors, other.ancestors, strict=True)
            )
        except ValueError:
            return False

    def compare_trees_and_nodes_positions(
        self,
        other: Tree[Enum, Enum, Any, Any],
    ) -> bool:
        """Return True if the trees, the calling node, and their position in their respective trees are the same."""
        return self.compare_trees(other) and self.path == other.path

    def compare_trees(
        self,
        other: Tree[Enum, Enum, Any, Any],
    ) -> bool:
        """Return true if the whole trees the nodes belong to are equal.

        Nodes themselves are not compared directly.
        """
        return self.root == other.root

    def compare_subtrees(
        self,
        other: Tree[Enum, Enum, Any, Any],
    ) -> bool:
        """Check if each node of two subtrees have the same content, shape, and the same element (Token or RulesTypes)."""
        return (
            self.compare_node(other)
            and len(self.children) == len(other.children)
            and all(a.compare_node(b) for a, b in zip(self.children, other.children, strict=True))
        )

    def compare_node(
        self,
        other: Tree[Enum, Enum, Any, Any],
    ) -> bool:
        """Check if two nodes have the same content (by checking (str) content, active_tokens_bounds and element)."""
        return (
            self.active_tokens_bounds == other.active_tokens_bounds
            and self._enum_compare(self.element, other.element)
            and self.content == other.content
        )

    def positions_are_equivalent(self, a: int, b: int) -> bool:
        """Return true if the two positions are only separated by whitespace, including (multiline or not) comments, or nothing.

        Max for a and b are the length of the content, corresponding to the position after the last character.
        """
        if not (0 <= a <= self.content_length and 0 <= b <= self.content_length):  # <= on purpose
            raise IndexError
        return a == b or a in self.tree_attributes.script_context.equivalent_positions[b]

    def token_indexes_are_equivalent(self, a: int, b: int) -> bool:
        """Return true if the two (full) token indexes are equivalents.

        Max for a and b is the number of tokens (including ignored tokens) content, \
        corresponding to the position after the last token.
        """
        if not (0 <= a <= self.token_length and 0 <= b <= self.token_length):  # <= on purpose
            raise IndexError
        return a == b or a in self.tree_attributes.script_context.equivalent_token_indexes[b]

    def __bool__(self) -> bool:
        """Return tree if there is at least one token in the tree."""
        return bool(self.active_token_content)

    @overload
    def get_nth_ancestor(self, level: Literal[-1]) -> Self:
        raise NotImplementedError

    @overload
    def get_nth_ancestor(self, level: int) -> Self:
        raise NotImplementedError

    def get_nth_ancestor(self, level: int) -> Self:
        """Pass -1 to level to get the root."""
        ret: Self = self
        if level == -1:
            while ret.parent is not None:
                assert ret.parent is not None
                ret = ret.parent
            return ret
        assert level >= 0
        ret2: Self = self
        for _ in range(level):
            if ret2.parent is None:
                raise IndexError
            ret2 = ret2.parent
        return ret2

    @overload
    def __getitem__(self, index: int) -> Self:
        raise NotImplementedError

    @overload
    def __getitem__(self, index: slice) -> list[Self]:
        raise NotImplementedError

    @overload
    def __getitem__(self, index: tuple[int, ...] | list[int]) -> Self:
        raise NotImplementedError

    @overload
    def __getitem__(
        self,
        index: MatchItem[TerminalType, RulesType, TreeDataType, NodeDataType],
    ) -> str:
        raise NotImplementedError

    def __getitem__(
        self,
        index: (int | slice | tuple[int, ...] | list[int] | MatchItem[TerminalType, RulesType, TreeDataType, NodeDataType]),
    ) -> list[Self] | Self | str:
        """Retrieve the n-th direct children when using an int as index.

        When index is a slice behave like doing node.children[index].
        A MatchItem can be used as index on a different Tree than the one it originates.
        """
        match index:
            case tuple() | list():
                ret = self
                for i in index:
                    assert isinstance(i, int)
                    ret = ret.children[i]
                return ret
            case MatchItem():
                if self.compare_trees(cast(Tree[Enum, Enum, Any, Any], index.root)):
                    return index.node.content[index.content_bounds]
                return self._cross_tree_getitem_matchitem(index)
            case int() | slice():  # slice with step might be useful. for comma separated lists for instance
                return self.children[index]
            case _: # pragma: no cover
                raise TypeError

    def _cross_tree_getitem_matchitem(
        self,
        index: MatchItem[TerminalType, RulesType, TreeDataType, NodeDataType],
    ) -> str:
        return self[index.path].content[index.content_bounds]

    def apply_match_item_relative_to_node(
        self,
        match_item: MatchItem[TerminalType, RulesType, TreeDataType, NodeDataType],
        *,
        get_node: bool = False,
    ) -> str | Self:
        """Follow the path, and get the node or its matching content by default."""
        node = self[match_item.path]
        return node if get_node else node.content[match_item.content_bounds]

    @overload
    def __contains__(
        self,
        other: Tree[Enum, Enum, Any, Any],
    ) -> bool:
        raise NotImplementedError

    @overload
    def __contains__(
        self,
        other: str,
    ) -> bool | list[MatchItem[TerminalType, RulesType, TreeDataType, NodeDataType]]:
        raise NotImplementedError

    @overload
    def __contains__(
        self,
        other: Pattern[str],
    ) -> list[MatchItem[TerminalType, RulesType, TreeDataType, NodeDataType]]:
        raise NotImplementedError

    @overload
    def __contains__(
        self,
        other: object,
    ) -> bool | list[MatchItem[TerminalType, RulesType, TreeDataType, NodeDataType]]:
        raise NotImplementedError

    def __contains__(
        self,
        other: object,
    ) -> bool | list[MatchItem[TerminalType, RulesType, TreeDataType, NodeDataType]]:
        """Warning : can be very long."""
        match other:
            case Tree():
                return self.contains_node(cast(Tree[Enum, Enum, TreeDataType, NodeDataType], other))
            case str() if (len(other) < SMALLEST_REGEX_STR_LEN or other[-1] != "/" or other[0] != "/"):
                return other.lower() in self.content.lower()
            case Pattern() if isinstance(cast(Pattern[bytes] | Pattern[str], other).pattern, bytes):
                return False
            case str() | Pattern():
                return ContentMatch(
                    self.content,
                    self,
                    regex_function=search,
                ).get_matches_against(cast(Pattern[str] | str, other))
            case Enum() | None:
                return any(self._enum_compare(element, other) for element in self.descendants_elements)
            case _:
                return False

    def contains_node(self, other: Tree[Enum, Enum, Any, Any]) -> bool:
        """__contains__ when other (possibly contained) is a Tree node.

        Return true if the possibly contaning node has a node N such that N == other.
        """
        if len(self.ancestors) >= len(other.ancestors):
            return False
        if not all(
            self._enum_compare(sa.element, oa.element)
            for sa, oa in zip(reversed(self.ancestors), reversed(other.ancestors), strict=False)
        ):
            return False
        sal = len(self.ancestors)
        dal = [node.element for node in other.ancestors[: -sal if sal else None][::-1]]
        current: list[Tree[TerminalType, RulesType, TreeDataType, NodeDataType]] = [self]
        next_: list[Tree[TerminalType, RulesType, TreeDataType, NodeDataType]] = []
        for a in dal:
            for node in current:
                for child in node.children:
                    if self._enum_compare(node.element, a) and other.content in child.content:
                        next_.append(child)  # noqa: PERF401
            current = next_
            next_ = []
        return any(node == other for node in current)

    def _check_unique_tree_attributes(
        self,
        *,
        allow_non_root: bool = False,
    ) -> None:
        assert allow_non_root or self.parent is None
        tree_attributes = self.tree_attributes
        for node in self:
            if node.tree_attributes is not tree_attributes:
                error_message = "Every node of the tree should have the same tree_attributes."
                raise RuntimeError(error_message)

    def check(self, *, allow_double_check: bool = False) -> Literal[True]:
        """Perform checks on all nodes, raising on error, and return True."""
        tree_attributes = self.tree_attributes
        if not allow_double_check and tree_attributes.state.checked:
            error_message = "Tree has already been checked."
            raise RuntimeError(error_message)
        self._check_unique_tree_attributes(allow_non_root=True)
        for node in self:
            assert not (self.children and self.token is not None)
            node.check_init()
        tree_attributes.state.building = False
        tree_attributes.state.checked = True
        return True

    def _check_cycle(self) -> bool:
        node: Tree[TerminalType, RulesType, TreeDataType, NodeDataType] | None = self
        passed_by: set[int] = set()
        while node is not None:
            if id(node) in passed_by:
                return True
            passed_by.add(id(node))
            node = node.parent
        return False

    def check_init(self) -> None:
        """Perform some checks on the Tree to see if it seems ill formed."""
        if getattr(self, "_token", _NotSet) is _NotSet:
            raise AssertionError
        if getattr(self, "_rule", _NotSet) is _NotSet:
            raise AssertionError
        if getattr(self, "_parent", _NotSet) is _NotSet:
            raise AssertionError
        if getattr(self, "_active_tokens_bounds", _NotSet) is _NotSet:
            raise AssertionError
        assert id(_NotSet) not in {id(v) for v in self.__dict__.values()}
        assert sum(int(e is None) for e in [self.token, self.rule]) >= 1
        if self.is_token:
            assert not isinstance(self.active_tokens_bounds, _NotSetType)
            assert not isinstance(self.tree_attributes.script_context, _NotSetType)
            assert len(self.tree_attributes.script_context.active_token_list[self.active_tokens_bounds]) == 1
            assert self.token is self.tree_attributes.script_context.active_token_list[self.active_tokens_bounds][0]
        assert not self._check_cycle(), "Cycle detected."
        assert len(self.active_token_content) == self.active_token_length
        assert len(self) == len(self.content)
        assert len(self.token_content) == self.token_length
        assert self.start_position is not None
        assert self.stop_position is not None
        assert self.start_position <= self.stop_position
        assert self.start_position <= self.stop_position

    def reload(self) -> None:
        """After modifications on any node of the tree, call this method to discard caches."""
        for node in self.get_nth_ancestor(-1):
            node._discard_cache()

    def __setattr__(self, name: str, value: object) -> None:
        """Prevent accidental modification on a locked tree. __setattr__ = object.__setattr__ is your friend."""
        state = self.tree_attributes.state
        if state.locked and name != "node_data":
            error_message = "Locked tree."
            raise AttributeError(error_message)
        if state.building and name not in object.__getattribute__(self, "_building_attributes") and name != "node_data":
            error_message = "Non building attribute."
            raise AttributeError(error_message)
        object.__setattr__(self, name, value)

    def __delattr__(self, name: str) -> None:
        """Prevent accidental modification on a locked tree."""
        if self.tree_attributes.state.locked and name != "node_data":
            error_message = "Locked tree."
            raise AttributeError(error_message)
        object.__delattr__(self, name)

    def add_children(self, *children: Self) -> None:
        """Link a parent and a child node, updating parent's children and child's parent."""
        existing_children: set[int] = {id(child) for child in self.children}
        for child in children:
            assert not isinstance(self.children, _NotSetType)
            assert id(child) not in existing_children
            existing_children.add(id(child))
            self.children.append(child)
            child._parent = self

    def update_from_leaves(self, *, attach_index: int = 0) -> None:
        """Update the active token bounds."""
        assert self._parent is None
        if callbacks := self._update_from_leaves():
            for callback in callbacks:
                callback(attach_index)

    def _update_from_leaves(
        self,
    ) -> list[Callable[[int], None]]:
        """For Tree that are Token, the active_tokens_bounds must be already set."""
        if self._token is not None and self._token is not _NotSet:
            return []
        start_ref: None | Self = None
        stop_ref: None | Self = None
        callbacks: list[Callable[[int], None]] = []
        for child in self.children:
            callbacks.extend(child._update_from_leaves())
            if isinstance(child._active_tokens_bounds, slice) and start_ref is None:
                start_ref = stop_ref = child
                for calllback in callbacks:
                    assert not isinstance(start_ref._active_tokens_bounds, _NotSetType)
                    calllback(start_ref._active_tokens_bounds.start)
                callbacks.clear()
            elif isinstance(child._active_tokens_bounds, slice):
                stop_ref = child
                for calllback in callbacks:
                    assert not isinstance(stop_ref._active_tokens_bounds, _NotSetType)
                    calllback(stop_ref._active_tokens_bounds.start)
                callbacks.clear()
        if start_ref is not None:
            assert stop_ref is not None
            assert start_ref._active_tokens_bounds is not None
            assert stop_ref._active_tokens_bounds is not None
            for calllback in callbacks:
                assert not isinstance(stop_ref._active_tokens_bounds, _NotSetType)
                calllback(stop_ref._active_tokens_bounds.stop)
            assert not isinstance(stop_ref._active_tokens_bounds, _NotSetType)
            assert not isinstance(start_ref._active_tokens_bounds, _NotSetType)
            self._active_tokens_bounds = slice(
                start_ref._active_tokens_bounds.start,
                stop_ref._active_tokens_bounds.stop,
            )
            return []
        else:

            def _set_ws_free_bound(bound: int) -> None:
                self._active_tokens_bounds = slice(bound, bound)

            callbacks.append(_set_ws_free_bound)
            return callbacks

    def process_tree_bottom_up[FResult](
        self,
        f: Callable[[Self], FResult],
    ) -> list[tuple[Self, FResult]]:
        """Apply a transformation such that it is never applied on a parent before it applied on the children."""
        ret: list[Self] = []
        current: list[Self] = [self]
        next_ones: list[Self] = []
        while current:
            for element in current:
                ret.append(element)
                next_ones.extend(element.children)
            current = next_ones
            next_ones = []
        results: list[tuple[Self, FResult]] = [(node, f(node)) for node in reversed(ret)]
        return results

    def add_childs_to_dict(
        self,
        *,
        max_number: int = MAX_CHILDS_AS_ATTRIBUTE,
    ) -> None:
        """For debugging purpose, add the children of every nodes of this tree as attributes of their parent.

        They are named 0, 1, 2, etc...
        """
        for node in self:
            for i, child in enumerate(node.children):
                if i >= max_number:
                    break
                setattr(node, f"{i}", child)

    def pretty_line(self, replaced_content: str, content_size: int) -> str:
        """Represent a single node without its hierarchy."""
        NNEWLINE = "\n"  # noqa: N806 pylint: disable=invalid-name
        DOUBLE_SLASH_N = "\\n"  # noqa: N806 pylint: disable=invalid-name
        return (
            f"from {self.start_position if self.start_position is not None else '?????':5} :   "
            f"{replaced_content.replace(NNEWLINE, DOUBLE_SLASH_N)[:content_size]:{content_size}}   -> "
            f"{self.stop_position if self.stop_position is not None else '?????':5}"
        )

    def pretty(
        self,
        *,
        max_compensation: int | None = 16,
        content_size: int = 32,
        add_context: bool = False,
    ) -> str:
        """Return a string representation of the whole subtree rooted on this node.

        Each nesting level produces 4 characters indentation.
        """
        if add_context:
            raise NotImplementedError
        ret: list[tuple[str, Callable[[], str], str]] = []
        max_level: int = 0

        def _filler(used: int) -> Callable[[], str]:
            l_used = used
            return lambda: (max_level - l_used) * 4 * " "

        @cache
        def _getindent(level: int) -> str:
            return "".join(["|*  " if not i % 4 else "|   " for i in range(level)])

        for node, level in self.depth_first_list_with_nexting_levels:
            filler = _filler(level)
            max_level = max(level, max_level)
            assert node.content is not None
            replaced_content = node.content.replace("\\", "\\\\")
            subcontent = (
                (node.rule.name if node.rule is not None else cast(TokenProtocol[TerminalType], node.token).token_type.name)
                if node.is_rule or node.is_token
                else "[None]"
            )
            ret.append(
                (
                    f"{_getindent(level)}{subcontent[:10]:10}",
                    filler,
                    node.pretty_line(replaced_content, content_size),
                ),
            )
        if max_compensation is not None:
            max_level = max(max_compensation, max_level)
        return "\n".join(" ".join([r[0], r[1](), r[2]]) for r in ret)

    __match_args__ = (
        "element",
        "has_unordered_elements_in_descendants",
        "regexable_content",
        "has_unordered_ancestors_rulestypes",
    )


@dataclass
class PicklingTree[TerminalType: Enum, RulesType: Enum, NodeDataType]:
    """Tree structure without reference to parent used to pickle Tree."""

    token: TokenProtocol[TerminalType] | None
    rule: RulesType | None
    children: list[Self]
    active_tokens_bounds: slice | _NotSetType
    node_data: NodeDataType | None

    def __hash__(self) -> int:  # noqa: D105
        return hash(
            (
                PicklingTree,
                self.token,
                self.rule,
                tuple(self.children),
                self.active_tokens_bounds,
                self.node_data,
            ),
        )
