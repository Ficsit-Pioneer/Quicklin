"""
Quicklin Transpiler — Converts Quicklin (.qko) source to Kotlin (.kt).

The transpiler operates in three phases:
  1. Tokenize the source (via the lexer)
  2. Transform keyword/type tokens using the mapping tables
  3. Emit the Kotlin output by joining transformed tokens

This approach guarantees that keywords inside strings, comments, and
partial identifiers are never modified.
"""

from __future__ import annotations

from .lexer import Token, TokenType, tokenize
from .keywords import IDENTIFIER_MAP, OPERATOR_MAP


def _transform_token(token: Token) -> Token:
    """
    Apply Quicklin → Kotlin mappings to a single token.

    Only IDENTIFIER and OPERATOR tokens are candidates for replacement.
    Everything else (strings, comments, whitespace, etc.) passes through
    unchanged.
    """
    if token.type == TokenType.IDENTIFIER:
        replacement = IDENTIFIER_MAP.get(token.value)
        if replacement is not None:
            return Token(type=token.type, value=replacement)

    elif token.type == TokenType.OPERATOR:
        replacement = OPERATOR_MAP.get(token.value)
        if replacement is not None:
            return Token(type=token.type, value=replacement)

    return token


def transpile(source: str) -> str:
    """
    Transpile a Quicklin source string to Kotlin.

    Args:
        source: The Quicklin (.qko) source code.

    Returns:
        The equivalent Kotlin (.kt) source code.

    Example:
        >>> from quicklin import transpile
        >>> transpile('fn main() { pr("Hello!") }')
        'fun main() { println("Hello!") }'
    """
    tokens = tokenize(source)
    transformed = [_transform_token(t) for t in tokens]
    return "".join(t.value for t in transformed)


def transpile_file(input_path: str, output_path: str | None = None) -> str:
    """
    Read a .qko file, transpile it, and optionally write a .kt file.

    Args:
        input_path:  Path to the input .qko file.
        output_path: Path for the output .kt file.  If None, the output
                     path is derived by replacing .qko → .kt.

    Returns:
        The transpiled Kotlin source code.
    """
    import pathlib

    inp = pathlib.Path(input_path)
    if output_path is None:
        out = inp.with_suffix(".kt")
    else:
        out = pathlib.Path(output_path)

    source = inp.read_text(encoding="utf-8")
    kotlin = transpile(source)
    out.write_text(kotlin, encoding="utf-8")
    return kotlin
