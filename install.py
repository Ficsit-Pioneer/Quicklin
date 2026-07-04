#!/usr/bin/env python3
"""
Quicklin Interactive Setup Wizard
==================================
A polished, step-by-step installer that:
  1. Checks system prerequisites (Python, OS)
  2. Detects or installs Kotlin
  3. Installs Quicklin as a CLI tool
  4. Adds Quicklin to the system PATH
  5. Registers the .qko file extension
  6. Configures user preferences
  7. Saves a config file and verifies everything works
"""

from __future__ import annotations

import ctypes
import json
import os
import pathlib
import platform
import shutil
import subprocess
import sys
import textwrap
import time
import winreg  # Windows-only, handled gracefully below

# ─── Constants ────────────────────────────────────────────────────────

VERSION = "1.0.0"
CONFIG_DIR = pathlib.Path.home() / ".quicklin"
CONFIG_FILE = CONFIG_DIR / "quicklin.config.json"
INSTALL_DIR = CONFIG_DIR / "bin"
IS_WINDOWS = platform.system() == "Windows"
IS_ADMIN = False

if IS_WINDOWS:
    try:
        IS_ADMIN = ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        IS_ADMIN = False


# ─── Color / Style Helpers ────────────────────────────────────────────

class Style:
    """ANSI escape code styling (graceful fallback on unsupported terminals)."""

    ENABLED = True

    # Try to enable ANSI on Windows 10+
    @staticmethod
    def _enable_ansi_windows():
        if not IS_WINDOWS:
            return
        try:
            kernel32 = ctypes.windll.kernel32
            handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
            mode = ctypes.c_ulong()
            kernel32.GetConsoleMode(handle, ctypes.byref(mode))
            kernel32.SetConsoleMode(handle, mode.value | 0x0004)  # ENABLE_VIRTUAL_TERMINAL_PROCESSING
        except Exception:
            Style.ENABLED = False

    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    ITALIC  = "\033[3m"
    UNDER   = "\033[4m"

    # Foreground
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"
    GRAY    = "\033[90m"

    # Background
    BG_BLUE   = "\033[44m"
    BG_GREEN  = "\033[42m"
    BG_RED    = "\033[41m"
    BG_YELLOW = "\033[43m"

    @classmethod
    def c(cls, code: str, text: str) -> str:
        if not cls.ENABLED:
            return text
        return f"{code}{text}{cls.RESET}"


Style._enable_ansi_windows()

S = Style  # shorthand


# ─── UI Helpers ───────────────────────────────────────────────────────

def clear_screen():
    os.system("cls" if IS_WINDOWS else "clear")


def banner():
    art = r"""
     ___        _      _    _ _
    / _ \ _   _(_) ___| | _| (_)_ __
   | | | | | | | |/ __| |/ / | | '_ \
   | |_| | |_| | | (__|   <| | | | | |
    \__\_\\__,_|_|\___|_|\_\_|_|_| |_|
    """
    print(S.c(S.CYAN + S.BOLD, art))
    print(S.c(S.BOLD, "    Ultra-Efficient Kotlin Shorthand Language"))
    print(S.c(S.DIM, f"    Version {VERSION}  |  Setup Wizard"))
    print()


def divider(char="─", width=56):
    print(S.c(S.DIM, char * width))


def step_header(num: int, total: int, title: str):
    print()
    divider()
    badge = S.c(S.BG_BLUE + S.WHITE + S.BOLD, f" Step {num}/{total} ")
    print(f"  {badge}  {S.c(S.BOLD, title)}")
    divider()
    print()


def success(msg: str):
    print(f"  {S.c(S.GREEN + S.BOLD, '[OK]')}  {msg}")


def warn(msg: str):
    print(f"  {S.c(S.YELLOW + S.BOLD, '[!!]')}  {msg}")


def error(msg: str):
    print(f"  {S.c(S.RED + S.BOLD, '[ERR]')} {msg}")


def info(msg: str):
    print(f"  {S.c(S.CYAN, '[i]')}  {msg}")


def ask_yes_no(prompt: str, default: bool = True) -> bool:
    hint = "[Y/n]" if default else "[y/N]"
    while True:
        raw = input(f"  {S.c(S.MAGENTA, '?')}  {prompt} {S.c(S.DIM, hint)} ").strip().lower()
        if raw == "":
            return default
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        warn("Please enter y or n.")


def ask_choice(prompt: str, options: list[str], default: int = 0) -> int:
    print(f"  {S.c(S.MAGENTA, '?')}  {prompt}")
    for i, opt in enumerate(options):
        marker = S.c(S.CYAN + S.BOLD, ">>") if i == default else "  "
        label = S.c(S.BOLD, opt) if i == default else opt
        print(f"      {marker} {S.c(S.DIM, f'[{i + 1}]')} {label}")
    while True:
        raw = input(f"      {S.c(S.DIM, f'Choice [1-{len(options)}]:')} ").strip()
        if raw == "":
            return default
        try:
            idx = int(raw) - 1
            if 0 <= idx < len(options):
                return idx
        except ValueError:
            pass
        warn(f"Enter a number between 1 and {len(options)}.")


def ask_input(prompt: str, default: str = "") -> str:
    hint = f" {S.c(S.DIM, f'[{default}]')}" if default else ""
    raw = input(f"  {S.c(S.MAGENTA, '?')}  {prompt}{hint} ").strip()
    return raw if raw else default


def progress_bar(label: str, duration: float = 1.5, steps: int = 30):
    """Simple animated progress bar."""
    print(f"  {label} ", end="", flush=True)
    for i in range(steps + 1):
        pct = i / steps
        filled = int(pct * 20)
        bar = S.c(S.GREEN, "█" * filled) + S.c(S.DIM, "░" * (20 - filled))
        print(f"\r  {label} [{bar}] {S.c(S.BOLD, f'{int(pct*100):>3}%')}", end="", flush=True)
        time.sleep(duration / steps)
    print()


# ─── Step 1: System Check ────────────────────────────────────────────

def step_system_check() -> bool:
    step_header(1, 7, "System Check")

    # Python version
    py_ver = sys.version_info
    if py_ver >= (3, 10):
        success(f"Python {py_ver.major}.{py_ver.minor}.{py_ver.micro} detected")
    else:
        error(f"Python {py_ver.major}.{py_ver.minor} detected — Quicklin requires Python 3.10+")
        return False

    # OS
    os_name = platform.system()
    os_ver = platform.version()
    success(f"Operating System: {os_name} {os_ver}")

    if IS_WINDOWS:
        if IS_ADMIN:
            success("Running as Administrator (full installation available)")
        else:
            warn("Running as standard user (file association will be per-user)")
    else:
        success(f"Platform: {platform.platform()}")

    # Architecture
    arch = platform.machine()
    success(f"Architecture: {arch}")

    return True


# ─── Step 2: Kotlin Detection / Installation ─────────────────────────

def _find_kotlin() -> str | None:
    """Try to find Kotlin on PATH."""
    kotlin = shutil.which("kotlinc")
    if kotlin:
        return kotlin
    kotlin = shutil.which("kotlin")
    if kotlin:
        return kotlin
    return None


def _get_kotlin_version(path: str) -> str:
    try:
        result = subprocess.run(
            [path, "-version"],
            capture_output=True, text=True, timeout=30,
        )
        output = result.stdout.strip() or result.stderr.strip()
        return output.split("\n")[0] if output else "unknown"
    except Exception:
        return "unknown"


def _install_kotlin_windows() -> bool:
    """Attempt to install Kotlin on Windows via popular package managers."""
    # Try Scoop first
    scoop = shutil.which("scoop")
    if scoop:
        info("Installing Kotlin via Scoop...")
        try:
            subprocess.run(["scoop", "install", "kotlin"], check=True, timeout=300)
            return True
        except Exception as e:
            warn(f"Scoop install failed: {e}")

    # Try Chocolatey
    choco = shutil.which("choco")
    if choco:
        info("Installing Kotlin via Chocolatey...")
        try:
            subprocess.run(["choco", "install", "kotlinc", "-y"], check=True, timeout=300)
            return True
        except Exception as e:
            warn(f"Chocolatey install failed: {e}")

    # Try winget
    winget = shutil.which("winget")
    if winget:
        info("Installing Kotlin via winget...")
        try:
            subprocess.run(
                ["winget", "install", "--id", "JetBrains.Kotlin.Compiler", "--accept-package-agreements", "--accept-source-agreements"],
                check=True, timeout=300,
            )
            return True
        except Exception as e:
            warn(f"winget install failed: {e}")

    return False


def _install_kotlin_unix() -> bool:
    """Attempt to install Kotlin on macOS/Linux via SDKMAN or brew."""
    # Try SDKMAN
    sdkman = pathlib.Path.home() / ".sdkman" / "bin" / "sdkman-init.sh"
    if sdkman.exists():
        info("Installing Kotlin via SDKMAN...")
        try:
            subprocess.run(
                ["bash", "-c", f"source {sdkman} && sdk install kotlin"],
                check=True, timeout=300,
            )
            return True
        except Exception as e:
            warn(f"SDKMAN install failed: {e}")

    # Try Homebrew (macOS)
    brew = shutil.which("brew")
    if brew:
        info("Installing Kotlin via Homebrew...")
        try:
            subprocess.run(["brew", "install", "kotlin"], check=True, timeout=300)
            return True
        except Exception as e:
            warn(f"Homebrew install failed: {e}")

    return False


def step_kotlin() -> bool:
    step_header(2, 7, "Kotlin Detection")

    kotlin_path = _find_kotlin()

    if kotlin_path:
        version = _get_kotlin_version(kotlin_path)
        success(f"Kotlin found: {kotlin_path}")
        success(f"Version: {version}")
        return True

    warn("Kotlin compiler (kotlinc) not found on PATH.")
    print()

    if not ask_yes_no("Would you like to install Kotlin now?"):
        info("Skipping Kotlin installation.")
        info("You can still use Quicklin to transpile .qko -> .kt files.")
        info("Install Kotlin later to compile the transpiled output.")
        return True

    print()
    info("Searching for package managers...")

    installed = False
    if IS_WINDOWS:
        installed = _install_kotlin_windows()
    else:
        installed = _install_kotlin_unix()

    if installed:
        success("Kotlin installed successfully!")
        # Verify
        kotlin_path = _find_kotlin()
        if kotlin_path:
            version = _get_kotlin_version(kotlin_path)
            success(f"Verified: {version}")
        return True
    else:
        warn("Could not auto-install Kotlin.")
        print()
        info("Manual installation options:")
        info("  Windows:  scoop install kotlin")
        info("           choco install kotlinc")
        info("           winget install JetBrains.Kotlin.Compiler")
        info("  macOS:    brew install kotlin")
        info("  Linux:    sdk install kotlin  (via SDKMAN)")
        info("  Manual:   https://kotlinlang.org/docs/command-line.html")
        print()
        info("Quicklin will still work for transpilation without Kotlin.")
        return True


# ─── Step 3: Install Quicklin Package ────────────────────────────────

def _get_project_root() -> pathlib.Path:
    """Find the project root (where setup.py lives)."""
    # Start from this script's location
    here = pathlib.Path(__file__).resolve().parent
    if (here / "setup.py").exists():
        return here
    # Fallback: CWD
    cwd = pathlib.Path.cwd()
    if (cwd / "setup.py").exists():
        return cwd
    return here


def step_install_package() -> bool:
    step_header(3, 7, "Install Quicklin Package")

    root = _get_project_root()
    info(f"Project root: {root}")

    choice = ask_choice(
        "Installation mode:",
        [
            "Development install (pip install -e .) -- recommended for local use",
            "Standard install (pip install .) -- recommended for production",
            "Skip package install (use python -m quicklin from project directory)",
        ],
        default=0,
    )

    print()

    if choice == 2:
        info("Skipping pip install. Use: python -m quicklin <file.qko>")
        return True

    editable = "-e" if choice == 0 else ""
    cmd = f"pip install {editable} .".strip() if editable else "pip install ."

    info(f"Running: {cmd}")
    progress_bar("Installing", duration=2.0)

    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install"] +
            (["-e", "."] if choice == 0 else ["."]),
            cwd=str(root),
            capture_output=True,
            text=True,
            check=True,
            timeout=120,
        )
        success("Quicklin package installed successfully!")

        # Verify the CLI is accessible
        quicklin_cmd = shutil.which("quicklin")
        if quicklin_cmd:
            success(f"CLI available at: {quicklin_cmd}")
        else:
            info("CLI 'quicklin' not on PATH yet (will be configured in next steps)")

        return True

    except subprocess.CalledProcessError as e:
        error("pip install failed:")
        if e.stderr:
            for line in e.stderr.strip().split("\n")[-5:]:
                print(f"      {S.c(S.DIM, line)}")
        warn("You can still use: python -m quicklin <file.qko>")
        return True
    except Exception as e:
        error(f"Installation error: {e}")
        return True


# ─── Step 4: Add to PATH ─────────────────────────────────────────────

def _get_scripts_dir() -> pathlib.Path:
    """Get the Python Scripts directory where CLI entry points live."""
    if IS_WINDOWS:
        return pathlib.Path(sys.prefix) / "Scripts"
    return pathlib.Path(sys.prefix) / "bin"


def _add_to_path_windows(directory: str) -> bool:
    """Add a directory to the user's PATH on Windows via the registry."""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Environment",
            0,
            winreg.KEY_READ | winreg.KEY_WRITE,
        )
        try:
            current_path, _ = winreg.QueryValueEx(key, "Path")
        except FileNotFoundError:
            current_path = ""

        # Check if already in PATH
        paths = [p.strip().lower() for p in current_path.split(";") if p.strip()]
        if directory.lower() in paths:
            success(f"Already in PATH: {directory}")
            winreg.CloseKey(key)
            return True

        # Append
        new_path = f"{current_path};{directory}" if current_path else directory
        winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
        winreg.CloseKey(key)

        # Broadcast the change so Explorer picks it up
        try:
            HWND_BROADCAST = 0xFFFF
            WM_SETTINGCHANGE = 0x001A
            SMTO_ABORTIFHUNG = 0x0002
            result = ctypes.c_long()
            ctypes.windll.user32.SendMessageTimeoutW(
                HWND_BROADCAST, WM_SETTINGCHANGE, 0,
                "Environment", SMTO_ABORTIFHUNG, 5000,
                ctypes.byref(result),
            )
        except Exception:
            pass

        success(f"Added to user PATH: {directory}")
        info("You may need to restart your terminal for PATH changes to take effect.")
        return True

    except PermissionError:
        error("Permission denied. Run as Administrator to modify PATH.")
        return False
    except Exception as e:
        error(f"Failed to modify PATH: {e}")
        return False


def _add_to_path_unix(directory: str) -> bool:
    """Add a directory to PATH via shell profile."""
    shell = os.environ.get("SHELL", "/bin/bash")
    if "zsh" in shell:
        profile = pathlib.Path.home() / ".zshrc"
    elif "fish" in shell:
        profile = pathlib.Path.home() / ".config" / "fish" / "config.fish"
    else:
        profile = pathlib.Path.home() / ".bashrc"

    export_line = f'\nexport PATH="{directory}:$PATH"  # Quicklin\n'

    # Check if already added
    if profile.exists():
        content = profile.read_text()
        if directory in content:
            success(f"Already in PATH ({profile.name})")
            return True

    with open(profile, "a") as f:
        f.write(export_line)

    success(f"Added to {profile.name}: export PATH=\"{directory}:$PATH\"")
    info(f"Run: source {profile}")
    return True


def step_add_to_path() -> bool:
    step_header(4, 7, "Add Quicklin to PATH")

    scripts_dir = _get_scripts_dir()
    project_root = _get_project_root()

    info(f"Python Scripts directory: {scripts_dir}")
    info(f"Quicklin project root:   {project_root}")
    print()

    # Check if quicklin CLI is already accessible
    quicklin_cmd = shutil.which("quicklin")
    if quicklin_cmd:
        success(f"'quicklin' command already on PATH: {quicklin_cmd}")
        if not ask_yes_no("Add project root to PATH as well?", default=False):
            return True

    dirs_to_add = []
    if not quicklin_cmd:
        dirs_to_add.append(str(scripts_dir))
    dirs_to_add.append(str(project_root))

    for d in dirs_to_add:
        if not ask_yes_no(f"Add to PATH: {d}?"):
            info(f"Skipping: {d}")
            continue

        if IS_WINDOWS:
            _add_to_path_windows(d)
        else:
            _add_to_path_unix(d)

    return True


# ─── Step 5: Register .qko File Extension ────────────────────────────

def _register_extension_windows() -> bool:
    """Register .qko file extension on Windows."""
    python_exe = sys.executable
    project_root = _get_project_root()

    try:
        # Method 1: Registry-based (per-user, no admin required)
        # Set .qko -> QuicklinFile
        key_ext = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\.qko")
        winreg.SetValue(key_ext, "", winreg.REG_SZ, "QuicklinFile")
        winreg.SetValueEx(key_ext, "Content Type", 0, winreg.REG_SZ, "text/x-quicklin")
        winreg.CloseKey(key_ext)

        # Set QuicklinFile properties
        key_type = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\QuicklinFile")
        winreg.SetValue(key_type, "", winreg.REG_SZ, "Quicklin Source File")
        winreg.CloseKey(key_type)

        # Set default icon (use Python's icon as a fallback)
        key_icon = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\QuicklinFile\DefaultIcon")
        winreg.SetValue(key_icon, "", winreg.REG_SZ, f"{python_exe},0")
        winreg.CloseKey(key_icon)

        # Set "Open" command — transpile the file
        key_open = winreg.CreateKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Classes\QuicklinFile\shell\open\command",
        )
        winreg.SetValue(key_open, "", winreg.REG_SZ, f'"{python_exe}" -m quicklin "%1" --stdout')
        winreg.CloseKey(key_open)

        # Set "Transpile" command in context menu
        key_transpile = winreg.CreateKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Classes\QuicklinFile\shell\transpile",
        )
        winreg.SetValue(key_transpile, "", winreg.REG_SZ, "Transpile to Kotlin")
        winreg.CloseKey(key_transpile)

        key_transpile_cmd = winreg.CreateKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Classes\QuicklinFile\shell\transpile\command",
        )
        winreg.SetValue(key_transpile_cmd, "", winreg.REG_SZ, f'"{python_exe}" -m quicklin "%1"')
        winreg.CloseKey(key_transpile_cmd)

        # Notify the shell of the change
        try:
            ctypes.windll.shell32.SHChangeNotify(0x08000000, 0x0000, None, None)
        except Exception:
            pass

        return True

    except PermissionError:
        error("Permission denied writing to registry.")
        return False
    except Exception as e:
        error(f"Registry error: {e}")
        return False


def _register_extension_unix() -> bool:
    """Register .qko MIME type and desktop entry on Linux."""
    try:
        # Add MIME type
        mime_dir = pathlib.Path.home() / ".local" / "share" / "mime" / "packages"
        mime_dir.mkdir(parents=True, exist_ok=True)

        mime_xml = mime_dir / "quicklin.xml"
        mime_xml.write_text(textwrap.dedent("""\
            <?xml version="1.0" encoding="UTF-8"?>
            <mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">
              <mime-type type="text/x-quicklin">
                <comment>Quicklin Source File</comment>
                <glob pattern="*.qko"/>
              </mime-type>
            </mime-info>
        """))

        # Update MIME database
        subprocess.run(
            ["update-mime-database", str(pathlib.Path.home() / ".local" / "share" / "mime")],
            capture_output=True,
        )

        return True
    except Exception as e:
        error(f"MIME registration failed: {e}")
        return False


def step_register_extension() -> bool:
    step_header(5, 7, "Register .qko File Extension")

    info("This associates .qko files with Quicklin so your OS recognizes them.")
    print()

    if IS_WINDOWS:
        info("The following will be configured in the Windows Registry:")
        info("  - .qko files recognized as 'Quicklin Source File'")
        info("  - Right-click context menu: 'Transpile to Kotlin'")
        info("  - Double-click: transpile and show Kotlin output")
    else:
        info("A MIME type (text/x-quicklin) will be registered for .qko files.")

    print()

    if not ask_yes_no("Register the .qko file extension?"):
        info("Skipping file extension registration.")
        return True

    progress_bar("Registering", duration=1.0)

    if IS_WINDOWS:
        ok = _register_extension_windows()
    else:
        ok = _register_extension_unix()

    if ok:
        success(".qko file extension registered!")
        if IS_WINDOWS:
            success("Context menu: Right-click any .qko file -> 'Transpile to Kotlin'")
    else:
        warn("File extension registration had issues (non-critical).")

    return True


# ─── Step 6: Preferences ─────────────────────────────────────────────

DEFAULT_CONFIG = {
    "version": VERSION,
    "preferences": {
        "default_output_dir": "",
        "auto_transpile": False,
        "preserve_qko_comments_in_output": True,
        "indent_style": "spaces",
        "indent_size": 4,
        "add_generated_header": True,
        "header_text": "// Generated by Quicklin v{version} — https://github.com/quicklin/quicklin",
        "color_output": True,
    },
    "paths": {
        "project_root": "",
        "kotlin_compiler": "",
        "python_executable": sys.executable,
    },
}


def step_preferences() -> dict:
    step_header(6, 7, "Preferences")

    info("Let's configure your Quicklin preferences.")
    info("You can change these later in: ~/.quicklin/quicklin.config.json")
    print()

    config = json.loads(json.dumps(DEFAULT_CONFIG))  # deep copy

    # 1. Auto-transpile
    config["preferences"]["auto_transpile"] = ask_yes_no(
        "Auto-transpile .qko files on save? (requires --watch mode)", default=False
    )

    # 2. Generated header
    print()
    config["preferences"]["add_generated_header"] = ask_yes_no(
        "Add a '// Generated by Quicklin' header to .kt output files?", default=True
    )

    # 3. Preserve comments
    print()
    config["preferences"]["preserve_qko_comments_in_output"] = ask_yes_no(
        "Preserve comments from .qko files in the transpiled .kt output?", default=True
    )

    # 4. Indent style
    print()
    indent_choice = ask_choice(
        "Indentation style for transpiled output:",
        ["Spaces (4)", "Spaces (2)", "Tabs"],
        default=0,
    )
    if indent_choice == 0:
        config["preferences"]["indent_style"] = "spaces"
        config["preferences"]["indent_size"] = 4
    elif indent_choice == 1:
        config["preferences"]["indent_style"] = "spaces"
        config["preferences"]["indent_size"] = 2
    else:
        config["preferences"]["indent_style"] = "tabs"
        config["preferences"]["indent_size"] = 1

    # 5. Default output directory
    print()
    out_dir = ask_input(
        "Default output directory for .kt files (blank = same as source):",
        default="",
    )
    config["preferences"]["default_output_dir"] = out_dir

    # 6. Color output
    print()
    config["preferences"]["color_output"] = ask_yes_no(
        "Enable colored CLI output?", default=True
    )

    # Fill in paths
    config["paths"]["project_root"] = str(_get_project_root())
    kotlin_path = _find_kotlin()
    config["paths"]["kotlin_compiler"] = kotlin_path or ""

    return config


# ─── Step 7: Save & Verify ───────────────────────────────────────────

def step_save_and_verify(config: dict) -> bool:
    step_header(7, 7, "Save Configuration & Verify")

    # Save config
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(config, indent=2), encoding="utf-8")
    success(f"Configuration saved to: {CONFIG_FILE}")

    # Verify transpiler works
    print()
    info("Running verification...")
    progress_bar("Verifying transpiler", duration=1.5)

    try:
        # Import and test
        sys.path.insert(0, str(_get_project_root()))
        from quicklin import transpile

        test_input = 'fn main() { pr("Hello, Quicklin!") }'
        test_output = transpile(test_input)
        expected = 'fun main() { println("Hello, Quicklin!") }'

        if test_output == expected:
            success("Transpiler verification passed!")
            print()
            info(f"  Input:  {S.c(S.CYAN, test_input)}")
            info(f"  Output: {S.c(S.GREEN, test_output)}")
        else:
            warn("Transpiler output differs from expected:")
            info(f"  Got:      {test_output}")
            info(f"  Expected: {expected}")

    except Exception as e:
        error(f"Verification failed: {e}")
        warn("The transpiler may still work — try: python -m quicklin <file.qko>")

    # Verify CLI
    print()
    quicklin_cmd = shutil.which("quicklin")
    if quicklin_cmd:
        success(f"CLI command 'quicklin' is on PATH: {quicklin_cmd}")
    else:
        info("CLI 'quicklin' not on PATH. Use: python -m quicklin <file.qko>")
        info("Restart your terminal if you added it to PATH in a previous step.")

    return True


# ─── Completion Screen ───────────────────────────────────────────────

def show_completion(config: dict):
    print()
    divider("=")
    print()
    print(S.c(S.GREEN + S.BOLD, "    Installation Complete!"))
    print()
    divider("=")
    print()

    print(S.c(S.BOLD, "  Quick Start:"))
    print()
    print(f"    {S.c(S.CYAN, '$')} quicklin hello.qko              {S.c(S.DIM, '# Transpile to hello.kt')}")
    print(f"    {S.c(S.CYAN, '$')} quicklin hello.qko --stdout     {S.c(S.DIM, '# Print Kotlin to terminal')}")
    print(f"    {S.c(S.CYAN, '$')} quicklin examples/              {S.c(S.DIM, '# Batch-transpile directory')}")
    print(f"    {S.c(S.CYAN, '$')} quicklin hello.qko --watch      {S.c(S.DIM, '# Auto-retranspile on save')}")
    print()
    print(f"    {S.c(S.DIM, 'Or use:  python -m quicklin <file.qko>')}")

    print()
    divider()
    print()
    print(S.c(S.BOLD, "  Useful Paths:"))
    print(f"    Config:     {S.c(S.CYAN, str(CONFIG_FILE))}")
    print(f"    Project:    {S.c(S.CYAN, config['paths']['project_root'])}")
    kotlin = config["paths"]["kotlin_compiler"]
    if kotlin:
        print(f"    Kotlin:     {S.c(S.CYAN, kotlin)}")
    print()
    divider()
    print()
    print(S.c(S.BOLD, "  Sample Quicklin Syntax:"))
    print()

    sample_qko = [
        ('dc User(vl name: Str, vl age: Int)', 'data class User(val name: String, val age: Int)'),
        ('fn greet(n: Str): Str {',            'fun greet(n: String): String {'),
        ('    rt "Hello, $n!"',                '    return "Hello, $n!"'),
        ('}',                                  '}'),
        ('vl x = name ?? "default"',           'val x = name ?: "default"'),
    ]
    max_qko = max(len(q) for q, _ in sample_qko)
    for qko, kt in sample_qko:
        print(f"    {S.c(S.CYAN, qko.ljust(max_qko))}  {S.c(S.DIM, '->')}  {S.c(S.GREEN, kt)}")

    print()
    divider()
    print()
    print(S.c(S.MAGENTA + S.BOLD, "  Happy coding with Quicklin!"))
    print(S.c(S.DIM, "  Write less. Do more. Ship faster."))
    print()


# ─── Main ─────────────────────────────────────────────────────────────

def main():
    clear_screen()
    banner()

    print(S.c(S.BOLD, "  Welcome to the Quicklin Setup Wizard!"))
    print()
    info("This wizard will guide you through installing and configuring Quicklin.")
    info("You can press Ctrl+C at any time to cancel.")
    print()

    if not ask_yes_no("Ready to begin?"):
        print()
        info("Setup cancelled. Run this script again when you're ready!")
        return

    try:
        # Step 1: System check
        if not step_system_check():
            error("System requirements not met. Aborting.")
            return

        # Step 2: Kotlin
        step_kotlin()

        # Step 3: Install package
        step_install_package()

        # Step 4: PATH
        step_add_to_path()

        # Step 5: File extension
        step_register_extension()

        # Step 6: Preferences
        config = step_preferences()

        # Step 7: Save & verify
        step_save_and_verify(config)

        # Done!
        show_completion(config)

    except KeyboardInterrupt:
        print()
        print()
        warn("Setup interrupted by user. Partial configuration may have been applied.")
        info(f"Config file: {CONFIG_FILE}")
        info("Re-run this script to complete setup.")


if __name__ == "__main__":
    main()
