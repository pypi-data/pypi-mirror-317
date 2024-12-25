"""Parse file at the path provided in the command line and print its tree."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import argh

from parser.memoize import FullParseResultType, parse_to_tree_with_cache
from parser.providers.lark import LarkParser
from parser.script_context import ScriptContext

from .cutter import get_unicode_offsets_and_encoded_str, get_valid_split_indexes
from .grammar import grammar
from .rules import RulesTypes
from .terminals import ignored_tokens
from .tokenizer import TokenType, tokenize


def main(only_one_path: str) -> None:
    """Parse the (single) file at the path provided as command line argument, to obtain a remerged tree."""
    with Path(only_one_path).open(encoding="utf-8") as file:
        provider: LarkParser[TokenType, RulesTypes] = LarkParser(grammar, RulesTypes)
        content = file.read()
        uo, es = get_unicode_offsets_and_encoded_str(content)
        tkl = tuple(tokenize(es, uo))
        sc = ScriptContext(content,  tkl, ignored_tokens)
        si = get_valid_split_indexes(sc, uo, es)
        tree: FullParseResultType[TokenType, RulesTypes, Any, Any, Any] = parse_to_tree_with_cache(
            provider,
            sc,
            si,
            (),
            None,
        )
        assert tree.rebuilt_parse_tree
        print(tree.rebuilt_parse_tree.pretty(), end=f'\n{"="*20}\n\n')  # noqa: T201

def run() -> None:
    """Run main with command line arguments."""
    argh.dispatch_command(main) #type: ignore

if __name__ == "__main__":
    run()
