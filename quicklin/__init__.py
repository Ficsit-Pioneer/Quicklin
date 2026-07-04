"""
Quicklin — Ultra-Efficient Kotlin Shorthand Language

A transpiled shorthand for Kotlin that lets you write Kotlin programs
with drastically fewer keystrokes. Every .qko file transpiles to valid,
idiomatic Kotlin.

Usage:
    python -m quicklin input.qko [-o output.kt]
"""

__version__ = "1.0.0"
__author__ = "Quicklin Contributors"

from .transpiler import transpile
from .keywords import KEYWORD_MAP, TYPE_MAP, OPERATOR_MAP

__all__ = ["transpile", "KEYWORD_MAP", "TYPE_MAP", "OPERATOR_MAP"]
