# Google AI Studio Auth — Circle the Square Project

## How image/video generation works
- Scripts use `google-genai` SDK with the `interactions.create()` endpoint
- This endpoint requires an **AQ. OAuth token** — NOT a plain API key
- The AQ. token is automatically set as `GEMINI_API_KEY` by the `agy` CLI
- AQ. tokens expire after a few hours — this is normal

## How to run scripts (always use the wrapper)
```powershell
python "C:/AI/Circle the Square/run_location_sheets.py"
```
This wrapper:
1. Calls `agy --print` to refresh the AQ. token
2. Reads the fresh token from `GEMINI_API_KEY` env var
3. Passes it (without `GOOGLE_API_KEY`) to the script subprocess

## If you get an auth error
1. Just re-run the wrapper: `python "C:/AI/Circle the Square/run_location_sheets.py"`
2. If it still fails, open a new `agy` session (the token refreshes on startup)
3. Never manually paste API keys — the wrapper handles everything

## Key files
- `C:\AI\Circle the Square\run_location_sheets.py` — one-click runner for all 9 location sheets
- `C:\AI\AI\refresh_google_token.py` — standalone token refresher (importable)
- `C:\AI\AI\gen_image.py` — reads AQ. token from `GEMINI_API_KEY` env var first

## What NOT to do
- ❌ Do NOT use `setx GEMINI_API_KEY` or `setx GOOGLE_API_KEY` — stale system env vars break auth
- ❌ Do NOT manually paste AQ. keys — they expire in hours
- ❌ Do NOT confuse Google AI Pro subscription (consumer) with API credits (separate billing)

## How auth works
- Google AI Pro subscription → agy login → AQ. token in `GEMINI_API_KEY` → scripts work
- The subscription is consumed via agy's OAuth2 session, NOT via API credits
- `oauth_creds.json` at `%USERPROFILE%\.gemini\oauth_creds.json` holds the refresh_token
