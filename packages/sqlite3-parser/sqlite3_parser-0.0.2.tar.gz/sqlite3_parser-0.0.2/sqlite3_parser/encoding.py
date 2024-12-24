"""Get encoded string and corresponding bytes-str offset and compensation fucntion."""

from __future__ import annotations

import bisect


def get_unicode_offsets_and_encoded_str(
    s: str,
) -> tuple[dict[int, int], bytes]:
    """Count each extra byte by appending the index several times to the returned list."""
    offsets: list[int] = []
    encoded_characters: list[bytes] = []
    for i, c in enumerate(s):
        encoded_character: bytes = c.encode("utf-8")
        length: int = len(encoded_character)
        if length > 1:
            offsets.extend([i] * (length - 1))
        encoded_characters.append(encoded_character)
    encoded = b"".join(encoded_characters)
    assert sorted(offsets) == offsets
    accrued_offsets: dict[int, int] = {index: i for i, index in enumerate(offsets, start=1)}
    return accrued_offsets, encoded


def compensate_offset(
    index: int,
    accrued_offsets: dict[int, int],
) -> int:
    """Return the corresponding index in the decoded string from the one in the encoded one."""
    keys = list(accrued_offsets)
    index_index = bisect.bisect_left(keys, index) - 1
    return index - accrued_offsets[keys[index_index]] if index_index >= 0 else index
