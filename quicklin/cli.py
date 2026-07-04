"""
Quicklin CLI — Command-line interface for the Quicklin transpiler.

Usage:
    python -m quicklin <input.qko>              # prints Kotlin to stdout
    python -m quicklin <input.qko> -o out.kt    # writes to out.kt
    python -m quicklin <directory>               # batch-transpile all .qko files
    python -m quicklin <input.qko> --watch       # watch for changes
"""

from __future__ import annotations

import argparse
import pathlib
import sys
import time

from .transpiler import transpile


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="quicklin",
        description="Quicklin → Kotlin transpiler.  Convert .qko files to .kt.",
        epilog="Examples:\n"
               "  python -m quicklin hello.qko\n"
               "  python -m quicklin hello.qko -o hello.kt\n"
               "  python -m quicklin examples/\n"
               "  python -m quicklin hello.qko --watch\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "input",
        help="A .qko file or a directory containing .qko files.",
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Output .kt file path (single-file mode only). "
             "Defaults to replacing the .qko extension with .kt.",
    )
    parser.add_argument(
        "--watch",
        action="store_true",
        help="Watch the input file(s) for changes and re-transpile automatically.",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print transpiled output to stdout instead of writing a file.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0",
    )
    return parser.parse_args(argv)


def _transpile_single(
    inp: pathlib.Path,
    out: pathlib.Path | None,
    *,
    to_stdout: bool = False,
) -> None:
    """Transpile one .qko file."""
    source = inp.read_text(encoding="utf-8")
    kotlin = transpile(source)

    if to_stdout:
        sys.stdout.write(kotlin)
        return

    if out is None:
        out = inp.with_suffix(".kt")

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(kotlin, encoding="utf-8")
    print(f"  [OK] {inp} -> {out}")


def _collect_qko_files(path: pathlib.Path) -> list[pathlib.Path]:
    """Collect all .qko files under a directory (recursive)."""
    return sorted(path.rglob("*.qko"))


def _transpile_batch(directory: pathlib.Path) -> None:
    """Transpile all .qko files in a directory tree."""
    files = _collect_qko_files(directory)
    if not files:
        print(f"No .qko files found in {directory}")
        return

    print(f"Transpiling {len(files)} file(s)...")
    for f in files:
        _transpile_single(f, None)
    print("Done!")


def _watch_loop(path: pathlib.Path, out: pathlib.Path | None) -> None:
    """Simple poll-based watch loop."""
    if path.is_dir():
        files = _collect_qko_files(path)
    else:
        files = [path]

    # Track modification times
    mtimes: dict[pathlib.Path, float] = {}
    for f in files:
        mtimes[f] = f.stat().st_mtime

    print(f"Watching {len(files)} file(s) for changes… (Ctrl+C to stop)")

    try:
        while True:
            time.sleep(0.5)
            # Re-scan directory for new files
            if path.is_dir():
                files = _collect_qko_files(path)

            for f in files:
                try:
                    current_mtime = f.stat().st_mtime
                except FileNotFoundError:
                    continue
                if f not in mtimes or current_mtime != mtimes[f]:
                    mtimes[f] = current_mtime
                    print(f"  [*] Change detected: {f}")
                    _transpile_single(f, out if not path.is_dir() else None)
    except KeyboardInterrupt:
        print("\nStopped watching.")


def main(argv: list[str] | None = None) -> None:
    """CLI entry point."""
    args = _parse_args(argv)
    inp = pathlib.Path(args.input)

    if not inp.exists():
        print(f"Error: '{inp}' does not exist.", file=sys.stderr)
        sys.exit(1)

    out = pathlib.Path(args.output) if args.output else None

    if args.watch:
        _watch_loop(inp, out)
    elif inp.is_dir():
        _transpile_batch(inp)
    else:
        _transpile_single(inp, out, to_stdout=args.stdout)


if __name__ == "__main__":
    main()
