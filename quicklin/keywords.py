"""
Quicklin → Kotlin keyword, type, and operator mappings.

All mappings are stored as ordered dictionaries so that longer tokens
are matched before shorter prefixes when necessary.
"""

# ─── Core Keyword Mappings ────────────────────────────────────────────
# Quicklin shorthand → Kotlin keyword
# Ordered longest-first within each starting letter to avoid prefix clashes.

KEYWORD_MAP: dict[str, str] = {
    # A
    "abs":   "abstract",
    "ann":   "annotation",
    # B
    "br":    "break",
    # C
    "cl":    "class",
    "cmp":   "companion",
    "cnt":   "continue",
    "ctch":  "catch",
    "ctr":   "constructor",
    # D
    "dc":    "data class",
    # E
    "el":    "else",
    "enm":   "enum",
    # F
    "fl":    "false",
    "fn":    "fun",
    "fnly":  "finally",
    "fr":    "for",
    # I
    "ifc":   "interface",
    "imp":   "import",
    "infx":  "infix",
    "inl":   "inline",
    "intl":  "internal",
    # L
    "ltnt":  "lateinit",
    # N
    "nl":    "null",
    # O
    "ob":    "object",
    "opn":   "open",
    "oprt":  "operator",
    "ovr":   "override",
    # P
    "pkg":   "package",
    "pr":    "println",
    "prt":   "protected",
    "prv":   "private",
    "pt":    "print",
    "pub":   "public",
    # R
    "rt":    "return",
    # S
    "seal":  "sealed",
    "sus":   "suspend",
    # T
    "thrw":  "throw",
    "tr":    "true",
    "ty":    "typealias",
    # V
    "vl":    "val",
    "vr":    "var",
    # W
    "wh":    "while",
    "wn":    "when",
}


# ─── Type Shortcuts ───────────────────────────────────────────────────
# Abbreviated type names → full Kotlin types.

TYPE_MAP: dict[str, str] = {
    "Str":   "String",
    "Bool":  "Boolean",
    "Dbl":   "Double",
    "Flt":   "Float",
    "Lng":   "Long",
    "Lst":   "List",
    "MLst":  "MutableList",
    "MMap":  "MutableMap",
    "MSet":  "MutableSet",
    "Arr":   "Array",
}


# ─── Operator Sugar ──────────────────────────────────────────────────
# Quicklin operator sequences → Kotlin operator sequences.
# These are replaced at the character level (not token level).

OPERATOR_MAP: dict[str, str] = {
    "??": "?:",   # Elvis / null coalesce
}


# ─── Combined Identifier Map (keywords + types) ─────────────────────
# Used by the transpiler for identifier-level replacements.

IDENTIFIER_MAP: dict[str, str] = {**KEYWORD_MAP, **TYPE_MAP}
