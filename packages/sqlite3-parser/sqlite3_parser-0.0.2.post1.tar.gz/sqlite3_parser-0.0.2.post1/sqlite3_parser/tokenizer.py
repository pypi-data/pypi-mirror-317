"""Produce a token list from a str."""

from __future__ import annotations

from collections.abc import Generator
from typing import Any

from parser.tree.protocols import AutoCalculatingToken

from .encoding import compensate_offset, get_unicode_offsets_and_encoded_str
from .terminals import ETokenType, TokenType
from .tokenizer_binding import tokenize_file_Binding


def tokenize(
    encoded_str: bytes,
    unicode_offsets: dict[int, int],
    *,
    omit_spaces_tokens: bool = False,
    allow_carriage_return: bool = False,
) -> Generator[AutoCalculatingToken[TokenType, tuple[ETokenType, Any]], None, None]:
    r"""Produce a token list from a str.

    On note que le \n terminant un inline comment n'est pas tokenizé dans cet inline comment.
    """
    if (not allow_carriage_return) and b"\r\n" in encoded_str:
        msg = r"Please strip any \r from input."
        raise ValueError(msg)
    raw_tokens: list[tuple[int, int, TokenType, ETokenType]] = tokenize_file_Binding(encoded_str)
    previous: AutoCalculatingToken[TokenType, tuple[ETokenType, Any]] | None = None
    for raw_start_position, raw_length, token_type, e_token_type in raw_tokens:
        if omit_spaces_tokens and token_type == TokenType.TK_SPACE:
            continue
        raw_end_position = raw_start_position + raw_length
        content = encoded_str[raw_start_position:raw_end_position].decode("utf-8")
        start_position = compensate_offset(raw_start_position, unicode_offsets)
        end_position = compensate_offset(raw_end_position, unicode_offsets)
        previous = AutoCalculatingToken(
            token_type=token_type,
            data=(e_token_type, None),
            content=content,
            start_position=start_position,
            stop_position=end_position,
            previous=previous,
        )
        yield previous


def main() -> None:
    o, e = get_unicode_offsets_and_encoded_str(input("Enter text (one line) to be tokenized."))
    print(*tokenize(e, o), sep="\n")  # noqa: T201


if __name__ == "__main__":
    main()


__all__ = [
    "tokenize",
]
