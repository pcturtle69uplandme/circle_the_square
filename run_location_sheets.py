"""Run generate_location_sheets.py with a freshly-refreshed Google OAuth token.

Just double-click this file or run:
    python run_location_sheets.py

It will:
1. Run a tiny agy command to wake up agy and get a fresh AQ. token
2. Read that fresh token from the environment / oauth_creds.json
3. Run generate_location_sheets.py with that token

No manual key management needed ever again.
"""

import sys
import os
import json
import subprocess
from pathlib import Path

LOCATION_SCRIPT = Path(r"C:\AI\Circle the Square\generate_location_sheets.py")
CREDS_FILE = Path(os.environ["USERPROFILE"]) / ".gemini" / "oauth_creds.json"


def get_fresh_token() -> str:
    """Run a tiny agy prompt to force agy to refresh its AQ. session token,
    then read it from the GEMINI_API_KEY environment variable that agy manages."""

    print("[1/2] Refreshing token via agy...")

    # agy --print refreshes its internal AQ. token and writes it to
    # GEMINI_API_KEY in its own process env. We capture that by running
    # a wrapper that echoes the env var after agy exits.
    result = subprocess.run(
        ["powershell", "-NoProfile", "-Command",
         "agy --print 'respond with only the word READY' | Out-Null; echo $env:GEMINI_API_KEY"],
        capture_output=True, text=True,
    )
    token = result.stdout.strip()

    if token and token.startswith("AQ."):
        print(f"[OK] Got fresh AQ. token: {token[:15]}... ({len(token)} chars)")
        return token

    # Fallback: use whatever is currently in this process's env
    token = os.environ.get("GEMINI_API_KEY", "")
    if token and token.startswith("AQ."):
        print(f"[OK] Using existing AQ. token from env: {token[:15]}...")
        return token

    sys.exit(
        "ERROR: Could not get a fresh AQ. token.\n"
        "Make sure agy is installed and you are logged in.\n"
        "Try opening a new agy session, then run this script again."
    )


def main():
    print("=" * 60)
    print("  Circle the Square — Location Sheet Generator")
    print("=" * 60)

    token = get_fresh_token()

    # Pass ONLY GEMINI_API_KEY with the fresh token.
    # Explicitly remove GOOGLE_API_KEY so it never overrides GEMINI_API_KEY.
    env = os.environ.copy()
    env["GEMINI_API_KEY"] = token
    env.pop("GOOGLE_API_KEY", None)

    print("\n[2/2] Running generate_location_sheets.py...\n")
    result = subprocess.run(
        [sys.executable, str(LOCATION_SCRIPT)],
        env=env,
        cwd=str(LOCATION_SCRIPT.parent),
    )

    if result.returncode == 0:
        print("\n[DONE] All location sheets generated successfully!")
    else:
        print(f"\n[WARN] Script exited with code {result.returncode}")
        print("If you see a 401/quota error, just run this script again.")
        print("If errors persist, close and reopen agy, then try again.")


if __name__ == "__main__":
    main()
