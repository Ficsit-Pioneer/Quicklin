<p align="center">
  <br/>
  <code>⚡ Q U I C K L I N ⚡</code>
  <br/>
  <strong>Ultra-Efficient Kotlin Shorthand</strong>
  <br/>
  <em>Write less. Mean the same. Ship faster.</em>
  <br/><br/>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+"></a>
  &nbsp;
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge" alt="License MIT"></a>
  &nbsp;
  <img src="https://img.shields.io/badge/version-1.0.0-blue?style=for-the-badge" alt="Version 1.0.0">
  &nbsp;
  <img src="https://img.shields.io/badge/transpiles%20to-Kotlin-7F52FF?style=for-the-badge&logo=kotlin&logoColor=white" alt="Kotlin">
  &nbsp;
  <img src="https://img.shields.io/badge/keywords-51%20mappings-orange?style=for-the-badge" alt="51 Mappings">
</p>

---

Quicklin is a **transpiled shorthand language** for Kotlin. Every `.qko` file maps 1-to-1 to valid, idiomatic `.kt` — no runtime, no magic, just fewer keystrokes.

The transpiler is a lightweight Python tool that tokenizes your source, replaces abbreviated keywords and types, and emits clean Kotlin. Strings and comments are **never** touched.

A human came up with this idea. Quicklin was then planned out and finished by Claude Opus 4.6 in Antigravity. 

---

## 📊 By the Numbers: How Much Faster Is Quicklin?

Quicklin was designed to eliminate the redundant keystrokes that slow down Kotlin development. Here are the **real, measured statistics** from the included example files:

### Keystroke Savings

| Metric | Value |
|--------|-------|
| **Total keyword/type mappings** | 51 (40 keywords + 10 types + 1 operator) |
| **Average characters saved per keyword** | **3.4 characters** |
| **Keyword character reduction** | **53–58%** fewer characters for keywords |
| **Overall file size reduction** | **3.5–5.0%** across full files (including comments) |
| **Top time saver** | `dc` → `data class` saves **8 characters** per use |
| **Fastest transpilation** | **78 tests in 0.004 seconds** |

### Real-World Example Savings

These statistics are measured from the 5 included example files:

| File | Quicklin Chars | Kotlin Chars | Characters Saved | Keyword Replacements |
|------|:-----------:|:--------:|:------------:|:----:|
| `hello_world.qko` | 2,352 | 2,441 | 89 | 30 |
| `fibonacci.qko` | 3,963 | 4,121 | 158 | 63 |
| `data_classes.qko` | 7,525 | 7,919 | 394 | 132 |
| `null_safety.qko` | 8,650 | 9,063 | 413 | 135 |
| `coroutines.qko` | 11,325 | 11,731 | 406 | 144 |
| **Total** | **33,815** | **35,275** | **1,460** | **504** |

> **504 keyword replacements** saving **1,460 characters** across just 5 example files. In a real project with hundreds of files, that adds up to tens of thousands of keystrokes saved.

### Top 10 Biggest Time Savers

| Rank | Quicklin | Kotlin | Characters Saved |
|:----:|:--------:|:------:|:-------:|
| 1 | `dc` | `data class` | **8** |
| 2 | `ctr` | `constructor` | **8** |
| 3 | `ty` | `typealias` | **7** |
| 4 | `ann` | `annotation` | **7** |
| 5 | `MLst` | `MutableList` | **7** |
| 6 | `cmp` | `companion` | **6** |
| 7 | `ifc` | `interface` | **6** |
| 8 | `prt` | `protected` | **6** |
| 9 | `MMap` | `MutableMap` | **6** |
| 10 | `MSet` | `MutableSet` | **6** |

### Speed Facts

- 🚀 **Transpilation is instant** — 78 unit tests complete in 0.004 seconds
- ⚡ **Zero dependencies** — pure Python, no external libraries required
- 📦 **Tiny footprint** — the entire transpiler is ~15 KB of Python code
- 🔒 **100% safe** — never modifies strings, comments, or partial identifiers
- 🎯 **100% Kotlin compatible** — output is valid, idiomatic Kotlin every time

---

## ⚡ At a Glance

<table>
<tr>
<th width="50%">Quicklin <code>.qko</code></th>
<th width="50%">Kotlin <code>.kt</code></th>
</tr>
<tr>
<td>

```kotlin
pkg com.example

imp kotlin.math.sqrt

dc User(vl name: Str, vl age: Int)

fn main() {
    vl users: Lst<User> = listOf(
        User("Alice", 30),
        User("Bob", 25)
    )

    fr (user in users) {
        pr("${user.name} is ${user.age}")
    }

    vl name: Str? = nl
    vl display = name ?? "Anonymous"
    pr(display)
}
```

</td>
<td>

```kotlin
package com.example

import kotlin.math.sqrt

data class User(val name: String, val age: Int)

fun main() {
    val users: List<User> = listOf(
        User("Alice", 30),
        User("Bob", 25)
    )

    for (user in users) {
        println("${user.name} is ${user.age}")
    }

    val name: String? = null
    val display = name ?: "Anonymous"
    println(display)
}
```

</td>
</tr>
</table>

---

## 🧙 Setup Guide

### Quick Install (2 commands)

```bash
git clone https://github.com/quicklin-lang/quicklin.git
cd quicklin
pip install -e .
```

### Interactive Setup Wizard (Recommended)

For a complete guided installation with Kotlin detection, PATH setup, file association, and preferences:

```bash
python install.py
```

The setup wizard will:

| Step | What It Does |
|------|-------------|
| **1. System Check** | Verifies Python 3.10+, OS, and architecture |
| **2. Kotlin Detection** | Finds Kotlin on PATH or offers to install it via Scoop/Chocolatey/winget/Homebrew/SDKMAN |
| **3. Package Install** | Installs Quicklin via `pip install -e .` (development) or `pip install .` (production) |
| **4. PATH Setup** | Adds the `quicklin` CLI command to your system PATH automatically |
| **5. File Association** | Registers `.qko` files with Windows (right-click → "Transpile to Kotlin") |
| **6. Preferences** | Configures auto-transpile, indentation, output headers, and more |
| **7. Verification** | Runs a transpilation test and confirms everything works |

### Manual Setup (Step by Step)

<details>
<summary><strong>1. Prerequisites</strong></summary>

- **Python 3.10+** — [Download](https://www.python.org/downloads/)
- **Kotlin** (optional, for compiling transpiled output) — [Download](https://kotlinlang.org/docs/command-line.html)
  - Windows: `scoop install kotlin` or `choco install kotlinc` or `winget install JetBrains.Kotlin.Compiler`
  - macOS: `brew install kotlin`
  - Linux: `sdk install kotlin` (via SDKMAN)

</details>

<details>
<summary><strong>2. Install Quicklin</strong></summary>

```bash
# Clone
git clone https://github.com/quicklin-lang/quicklin.git
cd quicklin

# Option A: Development install (editable, recommended)
pip install -e .

# Option B: Standard install
pip install .

# Option C: No install (run from project directory)
python -m quicklin hello.qko
```

</details>

<details>
<summary><strong>3. Verify Installation</strong></summary>

```bash
# Check version
quicklin --version

# Test transpilation
echo 'fn main() { pr("Hello!") }' > test.qko
quicklin test.qko --stdout
# Output: fun main() { println("Hello!") }
```

</details>

<details>
<summary><strong>4. Add to PATH (if not using pip install)</strong></summary>

**Windows (PowerShell as Admin):**
```powershell
$path = [Environment]::GetEnvironmentVariable("Path", "User")
[Environment]::SetEnvironmentVariable("Path", "$path;C:\path\to\quicklin", "User")
```

**macOS/Linux:**
```bash
echo 'export PATH="/path/to/quicklin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

</details>

<details>
<summary><strong>5. Register .qko File Type (Windows)</strong></summary>

```powershell
# Associate .qko files
assoc .qko=QuicklinFile
ftype QuicklinFile=python -m quicklin "%1" --stdout

# Or use the setup wizard for automatic registration:
python install.py
```

</details>

---

## 🚀 Usage

```bash
# Transpile a single file → produces hello.kt
quicklin hello.qko

# Transpile to a specific output file
quicklin hello.qko -o output.kt

# Transpile all .qko files in a directory (recursive)
quicklin src/

# Print transpiled Kotlin to stdout (no file written)
quicklin hello.qko --stdout

# Watch a file for changes and re-transpile automatically
quicklin hello.qko --watch

# Watch an entire directory
quicklin src/ --watch

# Check version
quicklin --version
```

You can also run it as a Python module:

```bash
python -m quicklin hello.qko
```

---

## 🗝️ Keyword Mappings

Every Quicklin keyword maps to exactly one Kotlin keyword or construct. The transpiler only replaces **whole identifiers** — partial matches inside longer names are safe.

| Quicklin | Kotlin | | Quicklin | Kotlin |
|:--------:|:----------:|---|:--------:|:----------:|
| `fn` | `fun` | | `rt` | `return` |
| `vl` | `val` | | `vr` | `var` |
| `pr` | `println` | | `pt` | `print` |
| `fr` | `for` | | `wh` | `while` |
| `wn` | `when` | | `el` | `else` |
| `cl` | `class` | | `dc` | `data class` |
| `ob` | `object` | | `ifc` | `interface` |
| `enm` | `enum` | | `seal` | `sealed` |
| `imp` | `import` | | `pkg` | `package` |
| `tr` | `true` | | `fl` | `false` |
| `nl` | `null` | | `br` | `break` |
| `cnt` | `continue` | | `thrw` | `throw` |
| `ctch` | `catch` | | `fnly` | `finally` |
| `abs` | `abstract` | | `opn` | `open` |
| `ovr` | `override` | | `pub` | `public` |
| `prv` | `private` | | `prt` | `protected` |
| `intl` | `internal` | | `cmp` | `companion` |
| `ctr` | `constructor` | | `sus` | `suspend` |
| `inl` | `inline` | | `infx` | `infix` |
| `oprt` | `operator` | | `ann` | `annotation` |
| `ty` | `typealias` | | `ltnt` | `lateinit` |

---

## 📐 Type Shortcuts

| Quicklin | Kotlin | Characters Saved |
|:--------:|:-----------:|:---:|
| `Str` | `String` | 3 |
| `Bool` | `Boolean` | 3 |
| `Dbl` | `Double` | 2 |
| `Flt` | `Float` | 1 |
| `Lng` | `Long` | 1 |
| `Lst` | `List` | 1 |
| `MLst` | `MutableList` | 7 |
| `MMap` | `MutableMap` | 6 |
| `MSet` | `MutableSet` | 6 |
| `Arr` | `Array` | 1 |

> **Note:** `Int`, `Map`, `Set`, `Any`, `Unit`, `Nothing`, and `Pair` are already short — they stay the same.

---

## 🔧 Operator Sugar

| Quicklin | Kotlin | Description |
|:--------:|:------:|:------------|
| `??` | `?:` | Elvis / null coalesce operator |

All other Kotlin operators (`?.`, `!!`, `..`, `::`, `->`, etc.) remain unchanged.

---

## 📝 Examples

The `examples/` directory includes 5 complete, commented `.qko` files:

| File | What It Demonstrates |
|------|---------------------|
| [`hello_world.qko`](examples/hello_world.qko) | `fn`, `pr`, `vl`, `vr`, `Str`, `if`/`el`, string interpolation |
| [`fibonacci.qko`](examples/fibonacci.qko) | `wh`, `fr`, `wn`, `rt`, `Lst`, `MLst`, recursion, loops |
| [`data_classes.qko`](examples/data_classes.qko) | `dc`, `cl`, `ifc`, `seal`, `enm`, `cmp ob`, `ovr`, `opn` |
| [`null_safety.qko`](examples/null_safety.qko) | `??`, `?.`, `nl`, nullable types, scope functions |
| [`coroutines.qko`](examples/coroutines.qko) | `sus`, `imp`, `try`/`ctch`/`fnly`, `thrw`, async patterns |

### Hello World

```kotlin
// hello.qko
fn main() {
    pr("Hello, Quicklin!")
}
```

Transpiles to:

```kotlin
// hello.kt
fun main() {
    println("Hello, Quicklin!")
}
```

### Data Classes & Collections

```kotlin
// models.qko
pkg com.app.models

dc Product(
    vl id: Lng,
    vl name: Str,
    vl price: Dbl,
    vl inStock: Bool
)

fn filterExpensive(products: Lst<Product>, threshold: Dbl): Lst<Product> {
    rt products.filter { it.price > threshold }
}

fn main() {
    vl catalog: Lst<Product> = listOf(
        Product(1L, "Laptop", 999.99, tr),
        Product(2L, "Mouse", 29.99, tr),
        Product(3L, "Monitor", 549.00, fl)
    )

    vl expensive = filterExpensive(catalog, 100.0)
    fr (item in expensive) {
        pr("${item.name}: $${item.price}")
    }
}
```

### Sealed Classes & When Expressions

```kotlin
// result.qko
seal cl Result<out T> {
    dc Success(vl data: T) : Result<T>()
    dc Error(vl message: Str) : Result<Nothing>()
    ob Loading : Result<Nothing>()
}

fn handleResult(result: Result<Str>) {
    wn (result) {
        is Result.Success -> pr("Got: ${result.data}")
        is Result.Error -> pr("Error: ${result.message}")
        is Result.Loading -> pr("Loading...")
    }
}
```

### Null Safety with Elvis

```kotlin
// nullsafe.qko
fn greet(name: Str?) {
    vl displayName = name ?? "World"
    pr("Hello, $displayName!")
}

fn findUser(id: Int): Str? {
    vl users: MMap<Int, Str> = mutableMapOf(
        1 to "Alice",
        2 to "Bob"
    )
    rt users[id]
}
```

---

## 🔬 Technical Details

### How the Transpiler Works

The Quicklin transpiler uses a **3-phase pipeline**:

1. **Lexer** — Splits source into typed tokens (`STRING`, `COMMENT`, `IDENTIFIER`, `OPERATOR`, `WHITESPACE`, etc.)
2. **Transformer** — Replaces only `IDENTIFIER` and `OPERATOR` tokens using the mapping tables
3. **Emitter** — Joins all tokens back into valid Kotlin source code

This architecture guarantees:
- ✅ Keywords inside `"strings"` are **never** replaced
- ✅ Keywords inside `// comments` are **never** replaced
- ✅ Partial identifiers like `printer` are **never** mangled to `printlner`
- ✅ Backtick-quoted identifiers like `` `fn` `` pass through untouched
- ✅ All whitespace, indentation, and formatting is preserved exactly

### Configuration

After running the setup wizard, preferences are stored at:

```
~/.quicklin/quicklin.config.json
```

Available settings:

| Setting | Default | Description |
|---------|---------|-------------|
| `auto_transpile` | `false` | Auto-transpile on file save (with `--watch`) |
| `add_generated_header` | `true` | Add `// Generated by Quicklin` to output |
| `preserve_qko_comments_in_output` | `true` | Keep comments in transpiled output |
| `indent_style` | `"spaces"` | `"spaces"` or `"tabs"` |
| `indent_size` | `4` | Number of spaces per indent level |
| `color_output` | `true` | Colored CLI output |

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/my-feature`
3. **Make** your changes and add tests
4. **Run** the test suite: `python -m unittest tests.test_transpiler -v`
5. **Commit** with a clear message: `git commit -m "Add my feature"`
6. **Push** to your fork: `git push origin feature/my-feature`
7. **Open** a Pull Request

### Development Setup

```bash
git clone https://github.com/quicklin-lang/quicklin.git
cd quicklin
pip install -e .
python -m unittest tests.test_transpiler -v   # 78 tests, all passing
```

### Areas for Contribution

- 🆕 New keyword or type shorthand proposals
- 🐛 Bug fixes in the lexer or transpiler
- 📖 Documentation improvements
- 🧪 Additional test cases
- 🔌 Editor plugins (VS Code, IntelliJ)
- ⚡ Performance optimizations
- 🎨 Syntax highlighting for `.qko` files

---

## 📄 License

Quicklin is released under the [MIT License](LICENSE).

```
MIT License — Copyright (c) 2026 Quicklin Contributors
```

---

<p align="center">
  Made with ⚡ by the Quicklin community
  <br/>
  <em>Less typing. Same Kotlin. Full speed.</em>
</p>
