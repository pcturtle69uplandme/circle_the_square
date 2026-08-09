# -*- coding: utf-8 -*-
"""
Utility: read Google Gemini API key from the Windows clipboard
and store it where the generation scripts expect it.

Usage:
    1. Copy your API key (e.g. ``AIza…``) to the clipboard.
    2. Run this script from the project root:
         python set_key_from_clipboard.py
    3. The key will be written to a ``.env`` file in the project root and
       exported as the environment variable ``GOOGLE_API_KEY`` for the current
       process.

If you only need the key for the current session, pass ``--export`` to avoid
writing a file.
"""

import os
import sys
import subprocess
from pathlib import Path

# Ensure pyperclip is available (works on Windows)
try:
    import pyperclip
except ImportError:
    print("[!] Installing pyperclip…")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyperclip"])
    import pyperclip


def get_key_from_clipboard() -> str:
    """Read the clipboard, strip whitespace, and return the key.
    Raises ValueError if the clipboard appears empty.
    """
    raw = pyperclip.paste()
    key = raw.strip()
    if not key:
        raise ValueError("Clipboard is empty – copy your Google API key first.")
    return key


def write_env(key: str, env_dir: Path) -> None:
    """Write a minimal ``.env`` file containing the API key.
    Overwrites any existing file.
    """
    env_path = env_dir / ".env"
    env_path.write_text(f"GOOGLE_API_KEY={key}\n", encoding="utf-8")
    print(f"[+] .env written to {env_path}")


def export_key(key: str) -> None:
    """Export the key to the current Python process environment."""
    os.environ["GOOGLE_API_KEY"] = key
    print("[+] GOOGLE_API_KEY exported to current process.")


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Store Google Gemini API key from clipboard")
    parser.add_argument("--export", action="store_true", help="Only export to current process (no .env file)")
    parser.add_argument("--env-dir", default=".", help="Directory where .env should be created (default: project root)")
    args = parser.parse_args()

    try:
        key = get_key_from_clipboard()
    except ValueError as e:
        sys.exit(f"Error: {e}")

    if args.export:
        export_key(key)
    else:
        env_path = Path(args.env_dir).expanduser().resolve()
        write_env(key, env_path)
        # Optionally run the location‑sheet generator after setting the key
        print("[+] Running location sheet generator…")
        subprocess.run([sys.executable, "generate_location_sheets.py"], cwd=Path(__file__).parent, check=False)

if __name__ == "__main__":
    main()
