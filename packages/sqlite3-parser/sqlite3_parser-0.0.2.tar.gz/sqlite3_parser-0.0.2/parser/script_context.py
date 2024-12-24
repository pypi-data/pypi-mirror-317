"""Implement ScriptContext, that carry the informations and some utlities used by different part of the parsing chain."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from itertools import pairwise
from typing import Any, cast

from .tree.protocols import TokenProtocol


@dataclass
class ScriptContext[TerminalType: Enum]:
    """Carry the informations and some utlities used by different part of the parsing chain.

    It is expected that each character is covered by one and only one token (tokens are contiguous).
    """

    script: str
    token_list: tuple[TokenProtocol[TerminalType], ...]
    ignored_tokens_types: frozenset[TerminalType] = field(default_factory=frozenset)

    active_token_list: tuple[TokenProtocol[TerminalType], ...] = field(init=False)
    token_to_index: dict[TokenProtocol[TerminalType], int] = field(init=False)
    active_token_to_index: dict[TokenProtocol[TerminalType], int] = field(init=False)

    equivalent_positions: dict[int, list[int]] = field(init=False)
    equivalent_token_indexes: dict[int, list[int]] = field(init=False)

    _position_to_token_index: dict[int, int] = field(init=False)

    def __reduce__(self) -> str | tuple[Any, ...]:
        """Doesn't store indexes."""
        return (
            ScriptContext,
            (
                self.script,
                self.token_list,
                self.ignored_tokens_types,
            ),
        )

    def __hash__(self) -> int:  # noqa: D105
        return hash(
            (
                ScriptContext,
                self.script,
                self.token_list,
                self.ignored_tokens_types,
            ),
        )

    def __eq__(self, value: object) -> bool:  # noqa: D105
        return (
            isinstance(value, ScriptContext)
            and self.script == value.script
            and self.token_list == cast(ScriptContext[Enum], value).token_list
            and self.ignored_tokens_types == cast(ScriptContext[Enum], value).ignored_tokens_types
        )

    def build_positions_equivalences(self) -> None:
        """Build the dictionnaries used to tell if two positions are only separated by ignored tokens and are semantically equivalent."""  # noqa: E501
        current_position_group: list[int] = [0]
        current_token_group: list[int] = [0]
        p = i = -1
        for i, token in enumerate(self.token_list):
            self.equivalent_token_indexes[i] = current_token_group
            if token.token_type in self.ignored_tokens_types:
                for p in range(token.start_position, token.stop_position):
                    self.equivalent_positions[p] = current_position_group
            else:
                for p in range(token.start_position, token.stop_position):
                    self.equivalent_positions[p] = current_position_group
                    current_position_group = []
                self.equivalent_token_indexes[i] = current_token_group
                current_token_group = []
        self.equivalent_token_indexes[i + 1] = current_token_group
        self.equivalent_positions[p + 1] = current_position_group

    def __post_init__(self) -> None:  # noqa: D105
        if self.token_list:
            assert self.token_list[0].start_position == 0
            assert self.token_list[-1].stop_position == len(self.script)
        assert all(token_a.stop_position == token_b.start_position for token_a, token_b in pairwise(self.token_list))

        self.active_token_list = tuple(token for token in self.token_list if token.token_type not in self.ignored_tokens_types)

        self.equivalent_token_indexes = {}
        self.equivalent_positions = {}
        self.build_positions_equivalences()

        self.token_to_index = {token: i for i, token in enumerate(self.token_list)}
        self.active_token_to_index = {token: i for i, token in enumerate(self.active_token_list)}

        self._position_to_token_index = {token.stop_position: i for i, token in enumerate(self.token_list)}
        if self.token_list:
            self._position_to_token_index[self.token_list[0].start_position] = -1
        else:
            pass

    def get_token_index_from_start_position(self, position: int) -> int:
        """Retrieve the index of a token from its start position."""
        index = self._position_to_token_index[position] + 1
        assert index < len(self.token_list)
        return index

    def get_token_index_from_stop_position(self, position: int) -> int:
        """Retrieve the index of a token from its stop position."""
        index = self._position_to_token_index[position]
        assert index >= 0
        return index
