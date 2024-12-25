"""Cut script into statements, convert them into tree and cache the result for next call, before returning merged tree."""

from __future__ import annotations

import typing
from collections.abc import Iterable
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from itertools import pairwise
from pathlib import Path

from cache3 import DiskCache, MiniCache  # type: ignore

from .providers import Provider
from .script_context import ScriptContext
from .tree.classic_tree import ClassicTree
from .tree.protocols import ClassicalTokenProtocol
from .tree.tree import Tree, _NotSet

UPDATE_FREQUENCY = 10
SAVE_IMMEDIATELY_N_FIRST_STATEMENTS = 2


class ExcludedTokenError(Exception):
    """The merge roor didn't include one ore more token from the root."""


def split_query[TerminalType: Enum, TokenDataType](
    script_context: ScriptContext[TerminalType],
    split_index: list[int],
) -> list[
    tuple[
        str,
        tuple[ClassicalTokenProtocol[TerminalType, TokenDataType], ...],
        tuple[ClassicalTokenProtocol[TerminalType, TokenDataType], ...],
    ]
]:
    """Split the given script into chunks. Token in script_context MUST be ClassicalToken compatible tokens.

    :param script_context: script_context whose content will be split.
    :param split_index: character indexes at which the script will be split.
        The tokens lists will be split at the matching place.
    :return: a list of triplets for each section, composed of the script chunk, the tokens chunk, the active tokens chunks.

    Each chunk contains a whitespace free and non whitespace free Token list chunks, and a script chunk.
    The whitespaces between two chunks TODO.

    """
    if script_context.token_list:
        try:
            _ = script_context.token_list[0].start_column  # type: ignore
            _ = script_context.token_list[0].data  # type: ignore
        except AttributeError as error:
            error_message = "Please use ClassicalToken compatible token with memoize.py."
            raise TypeError(error_message) from error
    if not script_context.script:
        return [("", (), ())]
    split_bounds = pairwise([0, *split_index, len(script_context.script)])
    chunks: list[tuple[
        str,
        tuple[ClassicalTokenProtocol[TerminalType, TokenDataType], ...],
        tuple[ClassicalTokenProtocol[TerminalType, TokenDataType], ...],
    ]] = []
    for start, end in split_bounds:
        if end == start:
            chunks.append(("", (), ()))
            continue
        tokens_chunk_start: int = script_context.get_token_index_from_start_position(position=start)
        tokens_chunk_stop: int = script_context.get_token_index_from_stop_position(position=end) + 1

        tkl = typing.cast(tuple[ClassicalTokenProtocol[TerminalType, TokenDataType], ...], script_context.token_list)
        tokens_chunk: tuple[ClassicalTokenProtocol[TerminalType, TokenDataType], ...] = tuple(
            tkl[tokens_chunk_start:tokens_chunk_stop])

        atkl = typing.cast(tuple[ClassicalTokenProtocol[TerminalType, TokenDataType], ...], script_context.active_token_list)
        modified_tokens_chunk_start: int = tokens_chunk_start
        modified_tokens_chunk_stop: int = tokens_chunk_stop
        active_tokens_chunk_stop = (
            script_context.active_token_to_index[script_context.token_list[modified_tokens_chunk_stop - 1]] + 1
            if end != len(script_context.script)
            else len(script_context.active_token_list)
        )

        while modified_tokens_chunk_start < len(script_context.token_list):
            if script_context.token_list[modified_tokens_chunk_start].token_type not in script_context.ignored_tokens_types:
                active_tokens_chunk_start = script_context.active_token_to_index[
                    script_context.token_list[modified_tokens_chunk_start]]
                break
            modified_tokens_chunk_start += 1
        else:
            active_tokens_chunk_start = active_tokens_chunk_stop
        active_tokens_chunk: tuple[ClassicalTokenProtocol[TerminalType, TokenDataType], ...] = atkl[
            active_tokens_chunk_start:active_tokens_chunk_stop]

        chunk: tuple[
            str,
            tuple[ClassicalTokenProtocol[TerminalType, TokenDataType], ...],
            tuple[ClassicalTokenProtocol[TerminalType, TokenDataType], ...],
        ] = (
            script_context.script[start:end],
            tokens_chunk,  # tokens
            active_tokens_chunk,  # active tokens
        )
        chunks.append(chunk)
    return chunks


class CachingParser[TerminalType: Enum, TokenDataType, RulesType: Enum]:
    """Split the scripts into chunks, parse them separately and memoize the result.

    So that :
        * little change on a big script doesn't result in reparsing it entirely.
        * super linear parsing time of the parser doesn't become a problem.
    """

    def __init__(
        self,
        provider: Provider[TerminalType, RulesType],
        merge_root_path: typing.Iterable[int],
        cache_path: Path | str | None = None,
        shared_cache_size: int = 1<<26,  # counter in statement character
    ) -> None:
        """Set cache parameters.

        :param cache_path: Path | str | None = None: If specified, the cache will be saved on disk\
            and persist between executions. Otherwise the cache will stay in memory.
        :param shared_cache_size: int = 1_000_000: limit the total size of cached script to this amount in character.
        """
        # DiskCache | MiniCache
        self.cache = typing.cast(
            typing.MutableMapping[
                tuple[
                    bool,
                    tuple[int, ...],
                    str,
                    tuple[ClassicalTokenProtocol[TerminalType, TokenDataType], ...],
                ],
                ClassicTree[TerminalType, RulesType, None, None, TokenDataType],
            ],
            (
                DiskCache(
                    timeout=3600*24*365,
                    max_size=(1<<26),
                    directory=str(Path(cache_path).parent),
                    name=Path(cache_path).name,
                )
                if cache_path is not None
                else MiniCache("", max_size=(1<<26))
            ),
        )
        self.cache_path: Path | str | None = cache_path
        self.shared_cache_max_size: int = shared_cache_size
        self.provider: Provider[TerminalType, RulesType] = provider
        self.merge_root_path: tuple[int, ...] = tuple(merge_root_path)

    def cache_tree_and_subtree(
        self,
        chunk: str,
        script_context: ScriptContext[TerminalType],
        active_token_chunk_bounds: slice,
    ) -> None:
        """Store in cache the parsed tree."""
        active_tokens_list_chunk = typing.cast(
            tuple[ClassicalTokenProtocol[TerminalType, TokenDataType], ...],
            script_context.active_token_list[active_token_chunk_bounds],
        )
        assert sum(bool(element is None) for element in[
            self.cache[(True, self.merge_root_path, chunk, active_tokens_list_chunk)],
            self.cache[(False, self.merge_root_path, chunk, active_tokens_list_chunk)],
        ]) != 1
        if self.cache[(True, self.merge_root_path, chunk, active_tokens_list_chunk)] is not None:
            return

        tree: ClassicTree[TerminalType, RulesType, None, None, TokenDataType] = self.provider.parse(
            typing.cast(tuple[ClassicalTokenProtocol[TerminalType, TokenDataType], ...], None),
            script_context,
            active_token_chunk_bounds,
            )
        tree._check_unique_tree_attributes()
        full: ClassicTree[TerminalType, RulesType, None, None, TokenDataType] = deepcopy(tree)
        partial: Tree[TerminalType, RulesType, None, None] = typing.cast(
            ClassicTree[TerminalType, RulesType, None, None, TokenDataType],
            ClassicTree,
        ).duck_copy(tree[self.merge_root_path].get_detached_subtree_copy())
        del tree
        if partial.active_tokens_bounds != full.active_tokens_bounds:
            error_message = "The enclosed token by tree and tree[merge_root_path] should be the same."
            raise ExcludedTokenError(error_message)

        full._check_unique_tree_attributes()
        full.tree_attributes.script_context = typing.cast(ScriptContext[TerminalType], None)
        full.reload()
        full.tree_attributes.state.building = True
        full.tree_attributes.state.locked = False
        self.cache[(True, self.merge_root_path, chunk, active_tokens_list_chunk)] = full

        partial._check_unique_tree_attributes()
        partial.tree_attributes.script_context = typing.cast(ScriptContext[TerminalType], None)
        partial.reload()
        partial.tree_attributes.state.building = True
        partial.tree_attributes.state.locked = False
        self.cache[(False, self.merge_root_path, chunk, active_tokens_list_chunk)] = partial

    def memoized_parse_chunk(
        self,
        chunk: str,
        script_context: ScriptContext[TerminalType],
        active_tokens_bounds: slice,
        *,
        get_full_tree: bool = False,
    ) -> tuple[
        ClassicTree[TerminalType, RulesType, None, None, TokenDataType],
        list[typing.Callable[[int], None]],
    ]:
        """Return the Tree obtained from parsing the chunk, parsing only if the result is not in cache."""
        self.cache_tree_and_subtree(
            chunk,
            script_context,
            active_tokens_bounds,
        )

        ret = deepcopy(self.cache[(
                get_full_tree,
                self.merge_root_path,
                chunk,
                typing.cast(
                    tuple[ClassicalTokenProtocol[TerminalType, TokenDataType], ...],
                    script_context.active_token_list[active_tokens_bounds],
                ),
            )])
        ret._set_active_bound_start_to(active_tokens_bounds.start)
        ret._check_unique_tree_attributes()
        ret.tree_attributes.script_context = script_context
        cbs = ret._update_from_leaves()
        ret._retrieve_script_context_token()
        ret.reload()
        ret._check_script_context_token()
        return ret, cbs

    def __call__(
        self,
        script_context: ScriptContext[TerminalType],
        split_indexes: list[int],
        *,
        pop_last_empty_if_s_non_empty: bool = False,
        lock_trees: bool = True,
    ) -> FullParseResultType[TerminalType, RulesType, typing.Any, typing.Any, TokenDataType]:
        """Produce the parse Tree and all the other informations from a string,\
            using memoization and cutting the string into smaller chunks for faster parsing.

        :param merge_root_path: list[int] | None = None: If specified, for each tree,\
            the children of the node at this path will be all merged under the node at this path of the first tree.\
            Otherwise, no merged tree will be returned.
        """  # noqa: D205
        if script_context.token_list:
            try:
                _ = script_context.token_list[0].start_column  # type: ignore
                _ = script_context.token_list[0].data  # type: ignore
            except AttributeError as error:
                error_message = "Please use ClassicalToken compatible token with memoize.py."
                raise TypeError(error_message) from error
        return self.get_remerged_tree_and_leftovers(
            script_context,
            split_indexes,
            lock_trees=lock_trees,
            pop_last_empty_if_s_non_empty=pop_last_empty_if_s_non_empty,
        )

    def script_to_trees(
        self,
        script_context: ScriptContext[TerminalType],
        split_indexes: list[int],
        *,
        pop_last_empty_if_s_non_empty: bool,
        first_full: bool = True,
    )-> tuple[list[ClassicTree[TerminalType, RulesType, typing.Any, typing.Any, TokenDataType]], ScriptContext[TerminalType]]:
        """Get deepcopy of script context and trees."""
        script_context = deepcopy(script_context)
        query_chunks: list[tuple[
                str,
                tuple[ClassicalTokenProtocol[TerminalType, TokenDataType], ...],
                tuple[ClassicalTokenProtocol[TerminalType, TokenDataType], ...],
        ]] = split_query(
            script_context,
            split_indexes,
        )

        trees: list[ClassicTree[TerminalType, RulesType, typing.Any, typing.Any, TokenDataType]] = []

        active_token_bounds: list[slice] = [slice(0, len(query_chunks[0][2]))]
        for _, _, active_tokens_chunk in query_chunks[1:]:
            previous = active_token_bounds[-1].stop
            active_token_bounds.append(slice(previous, previous + len(active_tokens_chunk)))

        first = True
        for chunk_triplet, atkb in zip(query_chunks, active_token_bounds, strict=True):
            tr, cbs = self.memoized_parse_chunk(
                chunk_triplet[0],
                script_context,
                atkb,
                get_full_tree=first_full and first,
            )
            if first:
                [cb(atkb.start) for cb in cbs]
            else:
                [cb(atkb.start) for cb in cbs]
            trees.append(tr)
            first = False

        if len(trees) > 1 and pop_last_empty_if_s_non_empty:
            trees.pop()

        return trees, script_context

    def get_merged_tree(
        self,
        script_context: ScriptContext[TerminalType],
        split_indexes: list[int],
        *,
        pop_last_empty_if_s_non_empty: bool,
    ) -> tuple[ClassicTree[TerminalType, RulesType, typing.Any, typing.Any, TokenDataType], ScriptContext[TerminalType]]:
        """pop_last_empty_if_s_non_empty should be False when the last active token isn't necessarily a separator."""
        trees, script_context = self.script_to_trees(
            script_context,
            split_indexes,
            pop_last_empty_if_s_non_empty=pop_last_empty_if_s_non_empty,
        )
        if any(trees) and trees:
            root = trees[0]
            merge_root = root[self.merge_root_path]
            for tree in trees[1:]:
                partial_tree = tree.children
                merge_root.add_children(*partial_tree)
            tree_attributes = trees[0].tree_attributes
            for node in [no for tr in trees for no in tr]:
                node.tree_attributes = tree_attributes
            root._retrieve_script_context_token()
            for node in root:
                if not node.is_token:
                    node._active_tokens_bounds = _NotSet
                    node._discard_cache()
            root.update_from_leaves()
            root.reload()
            root.check(allow_double_check=True)
            return root, script_context
        else:
            assert len(trees) <= 1
            if trees:
                root = trees[0]
                root.check(allow_double_check=True)
            else:
                raise NotImplementedError
            return root, script_context

    def get_remerged_tree_and_leftovers(  # noqa: D102
        self,
        script_context: ScriptContext[TerminalType],
        split_indexes: list[int],
        *,
        pop_last_empty_if_s_non_empty: bool,
        lock_trees: bool = True,
    ) -> FullParseResultType[TerminalType, RulesType, typing.Any, typing.Any, TokenDataType]:

        single_root, single_root_sc = self.get_merged_tree(
            script_context,
            split_indexes,
            pop_last_empty_if_s_non_empty=pop_last_empty_if_s_non_empty,
        )
        if lock_trees:
            single_root.tree_attributes.state.locked = lock_trees
        single_root.check(allow_double_check=True)

        left_leftover = script_context.script[: single_root.start_position]
        right_leftover = script_context.script[single_root.stop_position :]

        left_token_leftover: tuple[ClassicalTokenProtocol[TerminalType, TokenDataType], ...]
        right_token_leftover: tuple[ClassicalTokenProtocol[TerminalType, TokenDataType], ...]

        if single_root.start_position == single_root.stop_position == 0:
            left_token_leftover = typing.cast(
                tuple[ClassicalTokenProtocol[TerminalType, TokenDataType], ...], script_context.token_list)
            right_token_leftover = ()
        else:
            assert single_root.start_position is not None
            assert single_root.stop_position is not None
            left_token_leftover = typing.cast(
                tuple[ClassicalTokenProtocol[TerminalType, TokenDataType], ...],
                script_context.token_list)[: single_root.tokens_bounds.start]
            right_token_leftover = typing.cast(
                tuple[ClassicalTokenProtocol[TerminalType, TokenDataType], ...],
                script_context.token_list)[single_root.tokens_bounds.stop :]

        return FullParseResultType(
            single_root,
            single_root_sc,
            left_leftover,
            right_leftover,
            left_token_leftover,
            right_token_leftover,
        )


@dataclass
class FullParseResultType[TerminalType: Enum, RuleType: Enum, TreeDataType, NodeDataType, TokenDataType]:
    """Contain all the results obtained during treatment of a string, including parse tree(s)."""

    rebuilt_parse_tree: ClassicTree[TerminalType, RuleType, TreeDataType, NodeDataType, TokenDataType]
    rebuilt_parse_tree_sc: ScriptContext[TerminalType]
    leftover_left: str
    leftover_right: str
    left_token_leftover: tuple[ClassicalTokenProtocol[TerminalType, TokenDataType], ...]
    right_token_leftover: tuple[ClassicalTokenProtocol[TerminalType, TokenDataType], ...]

def parse_to_tree_with_cache[TerminalType: Enum, RulesType: Enum](  # noqa: PLR0913
    provider: Provider[TerminalType, RulesType],
    script_context: ScriptContext[TerminalType],
    split_indexes: list[int],
    merge_root_path: Iterable[int],
    cache_path: Path | str | None = None,
    shared_cache_size: int = 1<<26,
) -> FullParseResultType[TerminalType, RulesType, typing.Any, typing.Any, typing.Any]:
    """Set cache size and parse a script returning FullParseResultType instance in one call. Must always be called with the same parameters during one execution."""  # noqa: E501
    args = (
        cache_path,
        shared_cache_size,
    )

    class _Globals:
        def __init__(self) -> None:
            self.cache: CachingParser[TerminalType, typing.Any, RulesType] = CachingParser(
                provider,
                merge_root_path,
                cache_path,
                shared_cache_size,
            )
            self.first_params: tuple[typing.Any, ...] = args

    g = typing.cast(_Globals, getattr(parse_to_tree_with_cache, "cache", None))
    if g is None:
        g =  _Globals()
        setattr(parse_to_tree_with_cache, "cache", g)  # noqa: B010
    else:  # noqa: PLR5501
        if args != g.first_params:
            msg = (
                "Please keep the same parameters during execution when calling "
                "this function except for script parameter and merge root path."
            )
            raise RuntimeError(msg)
    return g.cache(
        script_context,
        split_indexes,
    )
