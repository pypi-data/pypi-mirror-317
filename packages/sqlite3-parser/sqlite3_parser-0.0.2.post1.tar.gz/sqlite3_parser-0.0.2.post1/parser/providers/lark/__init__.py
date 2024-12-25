"""Implement Lark parser provider.

Instanciate the provider with a grammar, and call parse on a script_context and active token list to get a ClassicTree.
"""
from __future__ import annotations

from collections.abc import Iterable
from enum import Enum
from typing import cast

from parser.script_context import ScriptContext
from parser.tree.classic_tree import ClassicalTokenProtocol, ClassicTree

from .tree_converter import LarkParser


def simple_parse_lark[TerminalType: Enum, RulesType: Enum, TokenDataType](
    full_tokens_list: Iterable[ClassicalTokenProtocol[TerminalType, TokenDataType]],
    ignored_tokens: frozenset[TerminalType],
    rules_enum: type[RulesType],
    grammar: str,
) -> ClassicTree[TerminalType, RulesType, None, None, TokenDataType]:
    """Produce a ClassicTree based AST from a token list.

    Lark earley parser is the default used parser.

    :param full_tokens_list: A list or iterable of the tokens obtained by tokenizing (lexing/scanning) the input (often text).
        The tokens should satisfie the ClassicalTokenProtocol.
        AutoCalculatingToken class can be used as it does satisfie this protocol.
        Ignored tokens (if there are) should be included in the iterable.
        The token_type field of each token should be part of an Enum representing the set of Terminals.
        The value of each members of this Enum should match a Terminal in the grammar.
        The terminals should be declared in the grammar (Lark grammar) using::

            %declare TerminalA TerminalB

        Ignored tokens can be declared but doesn't have to.
    :param ignored_tokens: A frozenset of every members of the Terminals Enum that are considered ignored (like whitespaces).
        Tokens having one of these as token_type will be stripped out when computing active_tokens_list \
            and will not be passed to Lark parser.
        A list of such Enum members can be converted to frozenset just by calling frozenset(ignored_list).
    :param rules_enum: An Enum.
        Every rules used in grammar must have a matching rules_enum member whose value is exactly the lowercase rule name.
    :param grammar: A `Lark context-free grammar <https://lark-parser.readthedocs.io/en/stable/grammar.html>`_, \
        possibly ambiguous.
        The start symbol is named "start" and should therefore have a production rule in the gramamr, \
            and a matching rules_enum member value should be the str "start".
        The grammar should not define any token.
        The rules should not contain any string_literal nor regexp_literal.

    |

    :return: The ClassicTree of the parse.
        Element attribute will be either a Terminal Enum member, a rules_enum member, or None.

    Given
        * an iterable of all (active and ignored) tokens
        * the ignored tokens types (terminals) frozenset
        * the rules Enumeration
        * and the lark grammar (with matching terminals name and ruled name)

    produce a ClassicTree based AST.
    """
    parser: LarkParser[TerminalType, RulesType] = LarkParser(grammar, rules_enum)
    sc = ScriptContext(
        "".join(token.content for token in full_tokens_list),
        tuple(full_tokens_list),
        ignored_tokens,
    )
    return parser.parse(
        cast(tuple[ClassicalTokenProtocol[TerminalType, TokenDataType]], sc.active_token_list),
        sc,
        slice(0, len(sc.active_token_list)),
    )

__all__ = [
    "simple_parse_lark",
]
