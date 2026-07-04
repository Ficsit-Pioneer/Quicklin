"""
Quicklin Lexer — Context-aware tokenizer.

Splits Quicklin source code into a stream of typed tokens so the
transpiler can safely replace keywords without touching strings,
comments, or partial identifiers.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum, auto
from typing import Iterator


# ─── Token Types ──────────────────────────────────────────────────────

class TokenType(Enum):
    """Categories of tokens produced by the lexer."""
    STRING = auto()          # "...", '...', \"\"\"...\"\"\", '''...'''
    CHAR_LITERAL = auto()    # 'x'
    COMMENT_LINE = auto()    # // ...
    COMMENT_BLOCK = auto()   # /* ... */
    IDENTIFIER = auto()      # keywords, variable names, type names
    NUMBER = auto()          # 42, 3.14, 0xFF, 1_000
    OPERATOR = auto()        # +, -, ??, ?:, ->, ::, etc.
    WHITESPACE = auto()      # spaces, tabs, newlines
    NEWLINE = auto()         # \n, \r\n
    PUNCTUATION = auto()     # { } ( ) [ ] , ; . :
    OTHER = auto()           # anything else


@dataclass(frozen=True, slots=True)
class Token:
    """A single lexer token."""
    type: TokenType
    value: str


# ─── Lexer Patterns ──────────────────────────────────────────────────
# Order matters: longer / more specific patterns first.

_PATTERNS: list[tuple[TokenType, re.Pattern[str]]] = [
    # Multi-line (triple-quoted) strings — must come before single-line strings
    (TokenType.STRING,        re.compile(r'\"\"\"[\s\S]*?\"\"\"')),
    (TokenType.STRING,        re.compile(r"\'\'\'[\s\S]*?\'\'\'")),

    # Single-line strings with escape handling
    (TokenType.STRING,        re.compile(r'"(?:[^"\\]|\\.)*"')),

    # Character literals: 'a', '\n', '\u00FF'
    (TokenType.CHAR_LITERAL,  re.compile(r"'(?:[^'\\]|\\.)'") ),

    # Block comments (possibly nested — we handle simple non-nested here)
    (TokenType.COMMENT_BLOCK, re.compile(r'/\*[\s\S]*?\*/')),

    # Line comments
    (TokenType.COMMENT_LINE,  re.compile(r'//[^\n]*')),

    # Newlines (tracked separately so formatting is preserved)
    (TokenType.NEWLINE,       re.compile(r'\r?\n')),

    # Whitespace (excluding newlines)
    (TokenType.WHITESPACE,    re.compile(r'[ \t]+')),

    # Numbers: hex, binary, float, int (with optional underscores)
    (TokenType.NUMBER,        re.compile(
        r'0[xX][0-9a-fA-F_]+[Ll]?'
        r'|0[bB][01_]+[Ll]?'
        r'|[0-9][0-9_]*\.[0-9][0-9_]*(?:[eE][+-]?[0-9_]+)?[fFdD]?'
        r'|[0-9][0-9_]*[eE][+-]?[0-9_]+[fFdD]?'
        r'|[0-9][0-9_]*[fFdDLl]'
        r'|[0-9][0-9_]*'
    )),

    # Identifiers (keywords, variable names, type names)
    # Kotlin allows backtick-quoted identifiers like `class`
    (TokenType.IDENTIFIER,    re.compile(r'`[^`]+`|[A-Za-z_]\w*')),

    # Multi-character operators (longest first)
    (TokenType.OPERATOR,      re.compile(
        r'\?\?'        # Quicklin null coalesce
        r'|\?\:'       # Kotlin elvis
        r'|\?\.'       # safe call
        r'|!!'         # non-null assert
        r'|\.\.'       # range
        r'|::'         # member reference
        r'|->'         # lambda arrow
        r'|<='         # less-or-equal
        r'|>='         # greater-or-equal
        r'|=='         # structural equality
        r'|!='         # structural inequality
        r'|==='        # referential equality
        r'|!=='        # referential inequality
        r'|\+='
        r'|-='
        r'|\*='
        r'|/='
        r'|%='
        r'|&&'         # logical and
        r'|\|\|'       # logical or
        r'|\+\+'       # increment
        r'|--'         # decrement
        r'|[+\-*/%=<>!&|^~?@#$]'
    )),

    # Punctuation
    (TokenType.PUNCTUATION,   re.compile(r'[{}()\[\],.;:]')),
]


# ─── Tokenizer ───────────────────────────────────────────────────────

def tokenize(source: str) -> list[Token]:
    """
    Tokenize a Quicklin source string into a list of Tokens.

    The tokenizer is greedy — at each position it tries every pattern
    in order and takes the first (longest) match.  Anything unmatched
    is emitted as TokenType.OTHER.
    """
    tokens: list[Token] = []
    pos = 0
    length = len(source)

    while pos < length:
        matched = False
        for token_type, pattern in _PATTERNS:
            m = pattern.match(source, pos)
            if m:
                tokens.append(Token(type=token_type, value=m.group()))
                pos = m.end()
                matched = True
                break

        if not matched:
            # Single unknown character — emit as OTHER
            tokens.append(Token(type=TokenType.OTHER, value=source[pos]))
            pos += 1

    return tokens
