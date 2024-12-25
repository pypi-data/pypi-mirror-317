"""Store the content of grammar.lark in grammar variable."""

from pathlib import Path

with (Path(__file__).parent / "grammar.lark").open(encoding="utf-8") as file:
    grammar = file.read()

__all__ = [
    "grammar",
]
