<#
.SYNOPSIS
  Reads a fal.ai API key from the clipboard and wires it up for both
  PowerShell sessions and the Node API scripts in fal-tools/api.

.USAGE
  1. Copy your fal.ai key (Settings -> Keys on fal.ai) to the clipboard.
  2. Run:  .\fal-tools\set-fal-key.ps1
  3. Re-open any terminal you want the persistent env var to appear in
     (the current session and the .env file are updated immediately;
     other already-open terminals are not).

  Never prints or logs the key in full - only a masked preview is shown.
#>

$ErrorActionPreference = "Stop"

$key = (Get-Clipboard -Raw).Trim()

if ([string]::IsNullOrWhiteSpace($key)) {
    Write-Error "Clipboard is empty. Copy your fal.ai API key first, then re-run this script."
}
if ($key -match '\s') {
    Write-Error "Clipboard content contains whitespace/newlines - that does not look like a single API key. Copy just the key value and re-run."
}
if ($key.Length -lt 16) {
    Write-Error "Clipboard content is too short to be a fal.ai API key ($($key.Length) chars). Copy the key from fal.ai -> Settings -> Keys and re-run."
}

function Mask([string]$s) {
    if ($s.Length -le 8) { return ('*' * $s.Length) }
    return $s.Substring(0,4) + ('*' * ($s.Length - 8)) + $s.Substring($s.Length - 4)
}

# 1. Current PowerShell session
$env:FAL_KEY = $key

# 2. Persistent user-level env var (visible to new terminals / processes after this)
[Environment]::SetEnvironmentVariable("FAL_KEY", $key, "User")

# 3. .env at repo root for Node scripts (fal-tools/api/*) - already gitignored, verified below
$repoRoot = Split-Path -Parent $PSScriptRoot
$envPath = Join-Path $repoRoot ".env"

$gitignorePath = Join-Path $repoRoot ".gitignore"
$gitignored = (Test-Path $gitignorePath) -and (Select-String -Path $gitignorePath -Pattern '^\.env$' -Quiet)
if (-not $gitignored) {
    Write-Error ".env is not confirmed gitignored in $gitignorePath - refusing to write the key to disk. Add .env to .gitignore first."
}

$lines = @()
if (Test-Path $envPath) {
    $lines = @(Get-Content $envPath | Where-Object { $_ -notmatch '^FAL_KEY=' })
}
$lines = @($lines) + @("FAL_KEY=$key")
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllLines($envPath, $lines, $utf8NoBom)

Write-Host "FAL_KEY set: $(Mask $key)" -ForegroundColor Green
Write-Host "  - current session: `$env:FAL_KEY"
Write-Host "  - persistent user env var (new terminals)"
Write-Host "  - $envPath (for fal-tools/api Node scripts via dotenv)"
