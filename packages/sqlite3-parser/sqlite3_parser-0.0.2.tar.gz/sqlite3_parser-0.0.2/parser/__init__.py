"""Regroup major reference of the parsing library.

* AutoCalculatingToken provide a valid dataclass based ClassicalTokenProtocol implementation,
    requiring just token_type, content, start_position, stop_position, data, and the preceding token (previous).
* parse perform a simple non cached and non split parse, returning a ClassicTree.
* parse_to_tree_with_cache does the same but with cache, and expecting token indexes at which query should be split.
* CachingParser allows to use multiple diffeernt configurations at the same cache, including different cache file.
* BaseToken is a subclassable token that is a valid ClassicalTokenProtocol implementation,
    requiring to set manually each of its attributes.
* ScriptContext is required for splitting and parsing with CachingParser or parse_to_tree_with_cache.
    Each different script has a different ScriptContext.
"""
from .memoize import CachingParser, parse_to_tree_with_cache
from .providers.lark import LarkParser as LarkProvider
from .providers.lark import simple_parse_lark as parse
from .script_context import ScriptContext
from .tree.protocols import AutoCalculatingToken, BaseToken
from .tree.tree import Tree
from .tree.tree_auxiliary import Predicate, Unordered

__all__ = [
    "AutoCalculatingToken",
    "parse",
    "LarkProvider",
    "CachingParser",
    "BaseToken",
    "parse_to_tree_with_cache",
    "ScriptContext",
    "Unordered",
    "Predicate",
    "Tree",
]
