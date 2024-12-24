"""Implements Singleton superclass."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator, Sequence
from dataclasses import dataclass, field
from enum import Enum
from itertools import count, product
from re import Match, Pattern, RegexFlag, fullmatch
from string import ascii_lowercase, digits
from typing import TYPE_CHECKING, Any, Literal, Self, cast, overload

from parser.script_context import ScriptContext

if TYPE_CHECKING:
    from .tree import Tree

MAX_CHILDS_AS_ATTRIBUTE = 30
SMALLEST_REGEX_STR_LEN = len("//")


class Singleton:
    """Base class for Singleton class."""

    def __new__(cls, *a: Any, **kwa: Any) -> Self:  # noqa: ANN401
        """Ensure a derived class is used."""
        if cls == Singleton:
            error_message = "Singleton must be used as superclass."
            raise TypeError(error_message)
        return super().__new__(cls, *a, **kwa)

    def __init_subclass__(cls) -> None:
        """Override new, making it return always the same instance."""
        super().__init_subclass__()
        instanciated = None
        original_new = cls.__new__

        def new_replacement(*args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
            nonlocal instanciated
            if instanciated is None:
                instanciated = original_new(*args, **kwargs)
                assert instanciated is not None
                return instanciated
            else:
                return instanciated

        cls.__new__ = new_replacement  # type: ignore

    def __reduce__(self) -> str | tuple[Any, ...]:
        """Unsure if object.__new__ is the default."""
        return (
            self.__class__,
            (),
        )


class UninitializedError(AttributeError):
    """Trying to access an uninitialized attribute, or to do computation with it."""

    def __init__(self, *args: object, **kwargs: Any) -> None:  # noqa: ANN401, D107
        assert UninitializedError.__doc__ is not None
        super().__init__(*args, **kwargs)
        self.add_note(UninitializedError.__doc__)


##############################################################################################################
##############################################################################################################


@dataclass
class MatchItem[TerminalType: Enum, RuleType: Enum, TreeDataType, NodeDataType]:
    """Path doesn't have to be the deepest containing element."""

    root: Tree[TerminalType, RuleType, TreeDataType, NodeDataType]
    path: list[int]  # from root to node
    node: Tree[TerminalType, RuleType, TreeDataType, NodeDataType]  # from which the search was performed
    content_bounds: slice  # relative to the above node
    index: int | None = None
    # if the match was done with finditer (or something that can produce several matches) the index of this match in the search
    match: Match[str] | None = None  # regex Match object


class ContentMatch[TerminalType: Enum, RuleType: Enum, TreeDataType, NodeDataType]:
    r"""'You need "(.|[\n])*" . And "/.../" ."""

    regex_function_type = Callable[[Pattern[str] | str, str, RegexFlag], Iterable[Match[str]] | Match[str] | None]

    @overload
    def __init__(
        self,
        content: str,
        node: Tree[TerminalType, RuleType, TreeDataType, NodeDataType],
        *,
        case_sensitive: bool = False,
        regex_function: regex_function_type = fullmatch,
        iterable_content: Literal[False] = False,
    ) -> None:
        raise NotImplementedError

    @overload
    def __init__(
        self,
        content: Iterable[str],
        node: Tree[TerminalType, RuleType, TreeDataType, NodeDataType],
        *,
        case_sensitive: bool = False,
        regex_function: regex_function_type = fullmatch,
        iterable_content: Literal[True] = True,
    ) -> None:
        raise NotImplementedError

    def __init__(
        self,
        content: str | Iterable[str],
        node: Tree[TerminalType, RuleType, TreeDataType, NodeDataType],
        *,
        case_sensitive: bool = False,
        regex_function: regex_function_type = fullmatch,
        iterable_content: bool = False,
    ) -> None:
        """Set the content to be searched against.

        The node can be the root of the Tree or a node that does the searc and matching.
        """
        super().__init__()
        self.case_sensitive = case_sensitive
        self.regex_function = regex_function
        self.node = node
        self.iterable_content = iterable_content
        if iterable_content:
            assert isinstance(content, Iterable)
            self.content = cast(Iterable[str], content)
        else:
            assert isinstance(content, str)
            self.content = cast(Iterable[str], [content])

    def get_matches_against(
        self,
        value: Pattern[str] | str,
    ) -> list[MatchItem[TerminalType, RuleType, TreeDataType, NodeDataType]]:
        """Return the list of successful matches as a MatchItem list.

        If value is of type Pattern, it it used in the regex function as pattern.
        If value starts and stops with a foward slash "/", value[1:-1] is used as a regex pattern.
        Otherwise the string is compared litterally.
        """
        flags: RegexFlag = RegexFlag.NOFLAG
        match value:
            case Pattern() as pattern:
                pass
            case str() if len(value) > 1 and value[-1] == value[0] == "/":
                flags |= RegexFlag.M if self.case_sensitive else RegexFlag.I | RegexFlag.M
                pattern = value[1:-1]
            case str():
                return [
                    MatchItem(
                        self.node.root,
                        self.node.path,
                        self.node,
                        slice(None, None),
                        index=i if self.iterable_content else None,
                    )
                    for i, content in enumerate(self.content)
                    if value == content
                ]
            case _: raise TypeError  # pragma: no cover  # noqa: E701
        ret: list[MatchItem[TerminalType, RuleType, TreeDataType, NodeDataType]] = []
        for i, content in enumerate(self.content):
            match = self.regex_function(
                pattern,
                content,
                flags,
            )
            try:
                ret.extend(
                    [
                        MatchItem(
                            self.node.root,
                            self.node.path,
                            self.node,
                            slice(m.start(), m.end()),
                            i if self.iterable_content else None,
                            m,
                        )
                        for m in cast(Iterable[Match[str]], match)
                    ],
                )
            except TypeError:
                if match is not None:
                    assert isinstance(match, Match)
                    ret.append(
                        MatchItem(
                            self.node.root,
                            self.node.path,
                            self.node,
                            slice(match.start(), match.end()),
                            match=match,
                        ),
                    )
        return ret

    def __eq__(self, value: object) -> bool:
        """Return True if there is at least one match."""
        if not isinstance(value, Pattern | str):
            return False
        return bool(self.get_matches_against(cast(Pattern[str] | str, value)))


class DynamicMatchAttributeHelper(Sequence[object]):
    """Match attribute comparaison target, meant to use a custom Callable as __eq__."""

    def __init__(
        self,
        match_test: Callable[[object], bool],
        *,
        auto_proxy_attributes: bool = True,
    ) -> None:
        """Create the helper and set its test to match_test.

        match_test will often maintain a closure on the Tree node.
        However theymight not if the value of the test only depends on the other.
        Or if they consider the tree frozen, they could pick one of several match_test function they have and use it.
        """
        super().__init__()
        self.auto_proxy_attributes: bool = auto_proxy_attributes
        self.match_test: Callable[[object], bool] = match_test

    def __eq__(self, value: object) -> bool:
        """Use the provided test function with the other value as only argument, and return directly its return value."""
        return self.match_test(value)

    def __getattribute__(self, name: str) -> Any:  # noqa: ANN401
        """Names are not stored (neither bound to match_test)."""
        if (not object.__getattribute__(self, "auto_proxy_attributes")) or name == "match_test":
            return object.__getattribute__(self, name)
        return self

    def __len__(self) -> Literal[2]:
        """Specializing the class for Sequences pattern mathing of len = 2."""
        return 2

    def __getitem__(self, key: int | slice) -> Any:  # noqa: ANN401
        """First call to match_test is ("min", value), second is ("max", value)."""
        if not isinstance(key, int):
            raise TypeError
        if key > 1:
            raise IndexError
        if key == 0:
            return DynamicMatchAttributeHelper(lambda o: self.match_test(("min", o)))
        else:
            return DynamicMatchAttributeHelper(lambda o: self.match_test(("max", o)))


class _SkippableType:
    def __getattr__(self, name: str) -> type:
        """Skippable.UnorderedXXX with XXX a number retrieves an Unordered with such capacity."""
        splits = name.split("rdered")
        ordered: bool
        match splits:
            case ["O", n] if all(c in digits for c in n):
                raise NotImplementedError
            case ["Uno", n] if all(c in digits for c in n):
                ordered = False
                if not n:
                    raise NameError
                capacity = int(n)
            case _:
                raise TypeError

        def match_args(c: int) -> Iterator[str]:
            for letters_number in count(1):  # pragma: no branch
                for letters_tuple in product(ascii_lowercase, repeat=letters_number):
                    if c == 0:
                        return
                    c -= 1
                    yield "".join(letters_tuple)

        del ordered

        class _UnorderedMeta(type):
            def __instancecheck__(cls, instance: object) -> bool:
                if DynamicMatchAttributeHelper in type(instance).__mro__:
                    return True
                return super().__instancecheck__(instance)

        class Unordered(metaclass=_UnorderedMeta):
            """Use in structural pattern matching case statement.

            This Unordered class has a positional match capacity determined by the name used to request it.
            Usage :::
                match something:
                    case Tree(_, Unordered(RulesTypes.SOME_RULE)):
                        print("matched")
            """

            __match_args__: tuple[str, ...] = tuple(match_args(capacity))

        return Unordered

    Unordered: type = __getattr__(cast(Self, None), "Unordered40")


Skippable = _SkippableType()
if TYPE_CHECKING:
    class Unordered(DynamicMatchAttributeHelper):  # noqa: D101
        __match_args__ = (
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
            "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "aa", "ab",
            "ac", "ad", "ae", "af", "ag", "ah", "ai", "aj", "ak", "al", "am", "an")
    Unordered.__doc__ = _SkippableType.Unordered.__doc__
else:
    Unordered = _SkippableType.Unordered

##############################################################################################################
##############################################################################################################

class Predicate:
    """Construct a predicate object.

    To be used in structural pattern matching as predicate.all or predicate.any.
    Example ::

        def has_even_size(s: str) -> bool:
            return not len(s) % 2
        predicate = Predicate(has_even_size)
        match tree:
            case Tree(iterable_attribute=predicate.all):
                print(f"{tree} matched. All of its iterable_attribute element verified predicate.")

    """

    def __init__(
        self,
        predicate: Callable[[object], bool],
    ) -> None:
        """Build a Predicate instance from a predicate callable, possibly a function, possibly with a closure."""
        self.quantifier: Callable[[Iterable[object]], bool] | None = None
        self.predicate: Callable[[object], bool] = predicate

    def __getattr__(self, name: str) -> Predicate:
        """Implement the behavior desired for pattern matching.

        The return value in these cases are a new Predicate object with its quantifier set to a\
            value different from none, which can be used immediately for comparison.
        """
        map_ = {
            "All": all,
            "all": all,
            "Every": all,
            "every": all,

            "Any": any,
            "any": any,
            "Some": any,
            "some": any,
        }
        if name in map_:
            ret = Predicate(self.predicate)
            ret.quantifier = map_[name]
            return ret
        else:
            raise AttributeError

    def __eq__(self, other: object) -> bool:
        """Check that all or any of the contained object of other verify the predicate."""
        if isinstance(other, Iterable):
            assert self.quantifier is not None
            return self.quantifier(self.predicate(value) for value in cast(Iterable[object], other))
        return False

    def __call__(self, x: object) -> bool:
        """Equivalent to self.predicate(x)."""
        return self.predicate(x)


##############################################################################################################
##############################################################################################################


@dataclass
class _TreeSate:
    building: bool = True
    locked: bool = False
    checked: bool = False


@dataclass
class TreeAttributes[TerminalType: Enum, TreeDataType]:
    """Common attributes shared by each Tree node of a Tree."""

    def __hash__(self) -> int:
        """Ignores state and strict_comparison."""
        return hash((self.script_context, self.tree_data, self.active_token_remerge_character))

    script_context: ScriptContext[TerminalType]
    state: _TreeSate = field(default_factory=_TreeSate)
    tree_data: TreeDataType = None  # type: ignore
    active_token_remerge_character: str = " "
    strict_comparison: bool = False
