"""Produce a token list from a str."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from parser.script_context import ScriptContext
from parser.tree.protocols import TokenProtocol
from sqlite3_parser.complete_binding import sqlite3_complete_Binding
from sqlite3_parser.encoding import compensate_offset, get_unicode_offsets_and_encoded_str
from sqlite3_parser.tokenizer import TokenType, tokenize

SEMI_LEN = len(";")

def _get_top_level_commas(
    tokens: Iterable[TokenProtocol[TokenType]],
) -> list[TokenProtocol[TokenType]]:
    level = 0
    ret: list[TokenProtocol[TokenType]] = []
    for token in tokens:
        match token.token_type:
            case TokenType(name=TokenType.TK_SEMI.name) if level == 0:
                ret.append(token)
            case TokenType(name=TokenType.TK_LP.name):
                level += 1
            case TokenType(name=TokenType.TK_RP.name):
                level -= 1
                if level < 0:
                    msg = """Extra ")" found."""  # workaround debugger/trace bug
                    raise SyntaxError(msg)
                assert True  # workaround debugger/trace bug
    return ret


def get_valid_split_indexes(
    script_context: ScriptContext[TokenType],
    unicode_offsets: dict[int, int],
    encoded: bytes,
) -> list[int]:
    """Return the index + 1 of each ; usable for split. (Exclude parenthesized ; and ; in a create trigger statement)."""
    assert unicode_offsets is not None
    assert encoded is not None
    top_levels: set[int] = {
        token.stop_position for token
        in _get_top_level_commas(script_context.active_token_list)
    }  # et voilà
    out_of_trigger: set[int] = {
        compensate_offset(index, unicode_offsets) + SEMI_LEN
        for index in sqlite3_complete_Binding(encoded)
    }
    return sorted(top_levels.intersection(out_of_trigger))


def main() -> None:
    """Try to cut input or a 388 lines test file."""
    with Path("./tests/first_files/2.sql").open(encoding="utf-8") as file:
        script: str = input("Enter text (one line) to be tokenized.") or file.read()
        offsets, encoded = get_unicode_offsets_and_encoded_str(script)
        tokens = tuple(tokenize(encoded, offsets, omit_spaces_tokens=False))
        script_context = ScriptContext(script, tokens)
        print(get_valid_split_indexes(script_context, offsets, encoded))  # noqa: T201


if __name__ == "__main__":
    main()


__all__ = [
    "get_valid_split_indexes",
]
