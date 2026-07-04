# Quicklin Language Specification

**Version 1.0.0** · *The complete reference for the Quicklin shorthand language.*

---

## 1. Introduction

Quicklin is a **transpiled shorthand language** that maps directly to Kotlin. The philosophy is simple:

> **Write less. Mean the same. Ship faster.**

Every `.qko` source file transpiles to a semantically identical `.kt` file. Quicklin introduces:

- **Abbreviated keywords** — shorter tokens for Kotlin's reserved words
- **Type shortcuts** — concise names for common Kotlin types
- **Operator sugar** — alternative operators that map to Kotlin equivalents

Quicklin does **not** change Kotlin's semantics, control flow, type system, or standard library. It is a purely syntactic layer — the transpiler performs token-level substitution and emits valid, idiomatic Kotlin.

---

## 2. File Conventions

| Aspect | Convention |
|:-------|:-----------|
| Source extension | `.qko` |
| Output extension | `.kt` |
| Encoding | UTF-8 |
| Line endings | LF or CRLF (preserved) |

When transpiling `hello.qko`, the default output is `hello.kt` in the same directory.

---

## 3. Keyword Mappings

The transpiler replaces **whole identifier tokens** only. A token like `framing` will NOT be modified — only the standalone token `fr` maps to `for`.

### 3.1 Functions & Control Flow

| Quicklin | Kotlin | Description | Example (Quicklin) |
|:--------:|:------:|:------------|:-------------------|
| `fn` | `fun` | Function declaration | `fn greet() { }` |
| `rt` | `return` | Return statement | `rt 42` |
| `fr` | `for` | For loop | `fr (i in 0..9) { }` |
| `wh` | `while` | While loop | `wh (x > 0) { }` |
| `wn` | `when` | When expression | `wn (x) { 1 -> pr("one") }` |
| `el` | `else` | Else branch | `if (x) { } el { }` |
| `br` | `break` | Break out of loop | `br` |
| `cnt` | `continue` | Continue to next iteration | `cnt` |

### 3.2 Declarations & Types

| Quicklin | Kotlin | Description | Example (Quicklin) |
|:--------:|:------:|:------------|:-------------------|
| `vl` | `val` | Immutable variable | `vl name: Str = "Alice"` |
| `vr` | `var` | Mutable variable | `vr count = 0` |
| `cl` | `class` | Class declaration | `cl Animal(vl name: Str)` |
| `dc` | `data class` | Data class | `dc Point(vl x: Int, vl y: Int)` |
| `ob` | `object` | Object/singleton | `ob Config { }` |
| `ifc` | `interface` | Interface | `ifc Drawable { fn draw() }` |
| `enm` | `enum` | Enum class | `enm cl Color { RED, GREEN, BLUE }` |
| `seal` | `sealed` | Sealed class/interface | `seal cl Result { }` |
| `ty` | `typealias` | Type alias | `ty Name = Str` |

### 3.3 Modifiers & Visibility

| Quicklin | Kotlin | Description | Example (Quicklin) |
|:--------:|:------:|:------------|:-------------------|
| `pub` | `public` | Public visibility | `pub fn api() { }` |
| `prv` | `private` | Private visibility | `prv vl secret = 42` |
| `prt` | `protected` | Protected visibility | `prt fn hook() { }` |
| `intl` | `internal` | Internal visibility | `intl cl Engine { }` |
| `abs` | `abstract` | Abstract class/member | `abs cl Shape { }` |
| `opn` | `open` | Open for inheritance | `opn cl Base { }` |
| `ovr` | `override` | Override member | `ovr fn toString(): Str = "X"` |
| `cmp` | `companion` | Companion object | `cmp ob { }` |
| `inl` | `inline` | Inline function | `inl fn run(block: () -> Unit) { }` |
| `infx` | `infix` | Infix function | `infx fn to(other: Int): Pair<Int, Int> = Pair(this, other)` |
| `oprt` | `operator` | Operator overload | `oprt fn plus(other: Vec): Vec = ...` |

### 3.4 Object Lifecycle

| Quicklin | Kotlin | Description | Example (Quicklin) |
|:--------:|:------:|:------------|:-------------------|
| `ctr` | `constructor` | Secondary constructor | `ctr(name: Str) : this(name, 0)` |
| `ltnt` | `lateinit` | Late initialization | `ltnt vr adapter: Adapter` |
| `sus` | `suspend` | Coroutine suspend | `sus fn fetch(): Str { }` |

### 3.5 I/O

| Quicklin | Kotlin | Description | Example (Quicklin) |
|:--------:|:------:|:------------|:-------------------|
| `pr` | `println` | Print with newline | `pr("Hello!")` |
| `pt` | `print` | Print without newline | `pt("Enter: ")` |

### 3.6 Literals & Packages

| Quicklin | Kotlin | Description | Example (Quicklin) |
|:--------:|:------:|:------------|:-------------------|
| `tr` | `true` | Boolean true | `vl active: Bool = tr` |
| `fl` | `false` | Boolean false | `vl done: Bool = fl` |
| `nl` | `null` | Null literal | `vl x: Str? = nl` |
| `imp` | `import` | Import statement | `imp kotlin.math.sqrt` |
| `pkg` | `package` | Package declaration | `pkg com.example.app` |

### 3.7 Exception Handling

| Quicklin | Kotlin | Description | Example (Quicklin) |
|:--------:|:------:|:------------|:-------------------|
| `thrw` | `throw` | Throw exception | `thrw IllegalStateException("!")` |
| `ctch` | `catch` | Catch block | `try { } ctch (e: Exception) { }` |
| `fnly` | `finally` | Finally block | `try { } fnly { cleanup() }` |

### 3.8 Annotations

| Quicklin | Kotlin | Description | Example (Quicklin) |
|:--------:|:------:|:------------|:-------------------|
| `ann` | `annotation` | Annotation class | `ann cl MyAnnotation` |

---

## 4. Type Shortcuts

Type shortcuts replace **identifier tokens** that match common Kotlin types. They follow the same rules as keyword mappings — only whole tokens are replaced.

| Quicklin | Kotlin | Example (Quicklin) |
|:--------:|:------:|:-------------------|
| `Str` | `String` | `vl name: Str = "Alice"` |
| `Bool` | `Boolean` | `vl active: Bool = tr` |
| `Dbl` | `Double` | `vl pi: Dbl = 3.14159` |
| `Flt` | `Float` | `vl ratio: Flt = 0.5f` |
| `Lng` | `Long` | `vl bigNum: Lng = 1_000_000L` |
| `Lst` | `List` | `vl items: Lst<Str> = listOf("a")` |
| `MLst` | `MutableList` | `vl items: MLst<Int> = mutableListOf()` |
| `MMap` | `MutableMap` | `vl cache: MMap<Str, Int> = mutableMapOf()` |
| `MSet` | `MutableSet` | `vl seen: MSet<Str> = mutableSetOf()` |
| `Arr` | `Array` | `vl nums: Arr<Int> = arrayOf(1, 2, 3)` |

---

## 5. Operator Sugar

Operator sugar replaces **operator tokens** — these are matched at the operator level, not the identifier level.

| Quicklin | Kotlin | Description | Example |
|:--------:|:------:|:------------|:--------|
| `??` | `?:` | Elvis / null coalesce | `vl x = name ?? "default"` |

### Unchanged Operators

All other Kotlin operators pass through unmodified:

| Operator | Description |
|:--------:|:------------|
| `?.` | Safe call |
| `!!` | Non-null assertion |
| `..` | Range |
| `::` | Member reference |
| `->` | Lambda arrow |
| `===` / `!==` | Referential equality |
| `==` / `!=` | Structural equality |
| `&&` / `\|\|` | Logical operators |

---

## 6. What Stays the Same

Many Kotlin keywords and types are already concise. Quicklin does **not** shorten them:

### Unchanged Keywords

| Keyword | Reason |
|:--------|:-------|
| `if` | Already 2 characters |
| `is` | Already 2 characters |
| `in` | Already 2 characters |
| `as` | Already 2 characters |
| `by` | Already 2 characters |
| `do` | Already 2 characters |
| `try` | Already 3 characters, highly recognizable |
| `this` | Context-dependent, risky to abbreviate |
| `super` | Rare enough, clarity matters |
| `it` | Already 2 characters (lambda implicit parameter) |
| `where` | Rare (generic constraints) |
| `init` | Already short |
| `get` | Already short |
| `set` | Already short |
| `field` | Already short |
| `value` | Already short |

### Unchanged Types

| Type | Reason |
|:-----|:-------|
| `Int` | Already 3 characters |
| `Map` | Already 3 characters |
| `Set` | Already 3 characters |
| `Any` | Already 3 characters |
| `Unit` | Already 4 characters |
| `Nothing` | Rare usage |
| `Pair` | Already 4 characters |
| `Byte` | Already 4 characters |
| `Char` | Already 4 characters |
| `Short` | Already 5 characters |

---

## 7. String & Comment Handling

The Quicklin transpiler uses a **context-aware lexer** that tokenizes source code before performing any replacements. This guarantees safety:

### Strings Are Never Modified

```kotlin
// Quicklin source
vl msg: Str = "Use fn to define a function"
pr(msg)
```

Transpiles to:

```kotlin
// Kotlin output
val msg: String = "Use fn to define a function"
println(msg)
```

The string content `"Use fn to define a function"` is preserved verbatim — `fn` inside the string is **not** replaced with `fun`.

### Comments Are Never Modified

```kotlin
// Quicklin source
// fn is the Quicklin shorthand for fun
fn main() {
    pr("Hello!")  // pr prints a line
}
```

Transpiles to:

```kotlin
// Kotlin output
// fn is the Quicklin shorthand for fun
fun main() {
    println("Hello!")  // pr prints a line
}
```

Comments pass through unchanged. Only identifiers in executable code are replaced.

### Supported String Forms

The lexer correctly handles all Kotlin string forms:

| Form | Pattern | Example |
|:-----|:--------|:--------|
| Double-quoted | `"..."` | `"hello"` |
| Triple-quoted (raw) | `"""..."""` | `"""raw string"""` |
| Escape sequences | `\"`, `\n`, etc. | `"line1\nline2"` |
| String templates | `$var`, `${expr}` | `"Name: ${user.name}"` |
| Character literals | `'x'` | `'A'` |

### Block Comments

```kotlin
/* This is a block comment.
   Keywords like fn, vl, pr are NOT replaced here. */
fn main() { }
```

---

## 8. Transpilation Model

### 8.1 Token Types

The lexer produces these token types:

| Token Type | Description | Replaceable? |
|:-----------|:------------|:------------:|
| `IDENTIFIER` | Keywords, variable names, type names | ✅ Yes |
| `OPERATOR` | `+`, `-`, `??`, `?.`, `!!`, etc. | ✅ Yes |
| `STRING` | All string literals | ❌ No |
| `CHAR_LITERAL` | Character literals | ❌ No |
| `COMMENT_LINE` | `// ...` | ❌ No |
| `COMMENT_BLOCK` | `/* ... */` | ❌ No |
| `NUMBER` | Integer and float literals | ❌ No |
| `WHITESPACE` | Spaces, tabs | ❌ No |
| `NEWLINE` | Line endings | ❌ No |
| `PUNCTUATION` | `{ } ( ) [ ] , ; . :` | ❌ No |
| `OTHER` | Unrecognized characters | ❌ No |

### 8.2 Transpilation Phases

```
┌─────────────────┐     ┌──────────────────┐     ┌───────────────┐
│  Source (.qko)   │ ──▶ │  Lexer/Tokenizer │ ──▶ │  Token Stream │
└─────────────────┘     └──────────────────┘     └───────┬───────┘
                                                         │
                                                         ▼
                                                 ┌───────────────┐
                                                 │  Transformer  │
                                                 │  (apply maps) │
                                                 └───────┬───────┘
                                                         │
                                                         ▼
                                                 ┌───────────────┐
                                                 │  Emitter      │
                                                 │  (join tokens)│
                                                 └───────┬───────┘
                                                         │
                                                         ▼
                                                 ┌───────────────┐
                                                 │  Output (.kt) │
                                                 └───────────────┘
```

1. **Tokenize** — The lexer scans the source using ordered regex patterns, producing a list of typed tokens.
2. **Transform** — Each `IDENTIFIER` token is checked against `KEYWORD_MAP` + `TYPE_MAP`. Each `OPERATOR` token is checked against `OPERATOR_MAP`. All other tokens pass through unchanged.
3. **Emit** — The transformed tokens are joined by concatenating their `.value` fields, producing the output Kotlin source.

### 8.3 Matching Rules

- **Whole-token only**: The identifier `framing` is a single `IDENTIFIER` token with value `framing`. It does NOT match `fr` because the match requires an exact key lookup, not a prefix search.
- **Longest match**: The lexer is greedy — at each position it tries patterns in order and takes the first match.
- **Case sensitive**: All mappings are case-sensitive. `Str` maps to `String`, but `str` does not.

---

## 9. Grammar Notes

Quicklin's grammar is **identical to Kotlin's grammar** with the following terminal substitutions:

```
QuicklinKeyword  →  one of { abs, ann, br, cl, cmp, cnt, ctch, ctr, dc, el,
                             enm, fl, fn, fnly, fr, ifc, imp, infx, inl,
                             intl, ltnt, nl, ob, opn, oprt, ovr, pkg, pr,
                             prt, prv, pt, pub, rt, seal, sus, thrw, tr,
                             ty, vl, vr, wh, wn }

QuicklinType     →  one of { Str, Bool, Dbl, Flt, Lng, Lst, MLst, MMap,
                             MSet, Arr }

QuicklinOperator →  one of { ?? }
```

All other grammar productions (expressions, statements, declarations, type parameters, lambdas, etc.) follow the [Kotlin Language Specification](https://kotlinlang.org/spec/) exactly.

A valid Quicklin program is any program where:

1. Every Quicklin keyword/type/operator can be replaced by its Kotlin counterpart
2. The resulting text is a valid Kotlin program

There are no new syntax constructs, no macros, and no preprocessor directives.

---

## 10. Quick Reference Card

```
╔══════════════════════════════════════════════════════════════╗
║                    QUICKLIN CHEAT SHEET                     ║
╠══════════════════════════════════════════════════════════════╣
║  fn → fun          vl → val          vr → var              ║
║  rt → return       fr → for          wh → while            ║
║  wn → when         el → else         br → break            ║
║  cl → class        dc → data class   ob → object           ║
║  ifc → interface   enm → enum        seal → sealed         ║
║  pr → println      pt → print        imp → import          ║
║  pkg → package     tr → true         fl → false            ║
║  nl → null         ?? → ?:           Str → String          ║
║  Bool → Boolean    Dbl → Double      Flt → Float           ║
║  Lng → Long        Lst → List        Arr → Array           ║
║  MLst → MutableList  MMap → MutableMap  MSet → MutableSet  ║
╚══════════════════════════════════════════════════════════════╝
```

---

*Quicklin Language Specification v1.0.0 — Copyright © 2026 Quicklin Contributors — MIT License*
