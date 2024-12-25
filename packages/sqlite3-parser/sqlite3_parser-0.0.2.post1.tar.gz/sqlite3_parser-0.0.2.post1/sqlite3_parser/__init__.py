"""Regroups main SQLite flavoured SQL parsing references."""

if __name__ == "__main__" and not __package__:  # pragma: no cover
    from pathlib import Path
    from sys import path
    path.append(str(Path(__file__).parent.parent))

import sys
from importlib.util import find_spec

if not find_spec("cffi"):  # pragma: no cover
    print('use "pip install language_tree[sqlite3-parser]" to use sqlite3_parser.')  # noqa: T201
    sys.exit()

from parser.tree.classic_tree import ClassicTree

from .encoding import get_unicode_offsets_and_encoded_str
from .parser_and_memoizer import SQLiteParser
from .parser_and_memoizer import simple_parse as parse
from .rules import RulesTypes
from .sqlite_tree import SQLiteTree
from .tokenizer import ETokenType, TokenType, tokenize

__all__ = [
    "parse",
    "RulesTypes",
    "TokenType",
    "SQLiteParser",
    "ClassicTree",
    "ETokenType",
    "tokenize",
    "get_unicode_offsets_and_encoded_str",
    "SQLiteTree",
]
