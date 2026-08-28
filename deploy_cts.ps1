<#
Circle the Square — GitHub Pages Deployment Script
================================================
Deploys f01_bubble_studio.html + audio-refs/ + storyboard-frames/ to the docs/ folder
for GitHub Pages hosting at: https://pcturtle69uplandme.github.io/circle_the_square/

Usage: .\deploy_cts.ps1
#>

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$DocsDir  = Join-Path $RepoRoot "docs"
$AudioDir = Join-Path $RepoRoot "audio-refs"
$FrameDir = Join-Path $RepoRoot "storyboard-frames"

Write-Host "CTS GitHub Pages Deploy" -ForegroundColor Cyan
Write-Host "======================"

# ── 1. Clean docs/ ──────────────────────────────────────────────
if (Test-Path $DocsDir) {
    Write-Host "[1/5] Cleaning old docs/ ..." -NoNewline
    Remove-Item -Recurse -Force $DocsDir
    Write-Host " done" -ForegroundColor Green
} else {
    New-Item -ItemType Directory -Path $DocsDir | Out-Null
    Write-Host "[1/5] Created docs/"
}

# ── 2. Copy HTML viewer ─────────────────────────────────────────
Write-Host "[2/5] Copying HTML viewer ..." -NoNewline
Copy-Item (Join-Path $RepoRoot "f01_bubble_studio.html") $DocsDir
Write-Host " done" -ForegroundColor Green

# ── 3. Copy audio-refs (MP3 files) ────────────────────────────
Write-Host "[3/5] Copying audio-refs/ ..." -NoNewline
$targetAudio = Join-Path $DocsDir "audio-refs"
New-Item -ItemType Directory -Path $targetAudio -Force | Out-Null
if (Test-Path $AudioDir) {
    $mp3s = Get-ChildItem $AudioDir -Filter "*.mp3"
    if ($mp3s.Count -eq 0) {
        Write-Host " WARNING: no MP3 files found in audio-refs/" -ForegroundColor Yellow
    } else {
        $mp3s | ForEach-Object { Copy-Item $_.FullName -Destination $targetAudio }
        Write-Host " $($mp3s.Count) MP3 files" -ForegroundColor Green
    }
} else {
    Write-Host " WARNING: audio-refs/ not found, skipping" -ForegroundColor Yellow
}

# ── 4. Copy storyboard frames ──────────────────────────────────
Write-Host "[4/5] Copying storyboard-frames/ ..." -NoNewline
$targetFrames = Join-Path $DocsDir "storyboard-frames"
New-Item -ItemType Directory -Path $targetFrames -Force | Out-Null
if (Test-Path $FrameDir) {
    $jpgs = Get-ChildItem $FrameDir -Filter "*.jpg" | Where-Object { $_.Directory.Name -ne "legacy_backup" }
    if ($jpgs.Count -eq 0) {
        Write-Host " WARNING: no JPG files found" -ForegroundColor Yellow
    } else {
        $jpgs | ForEach-Object { Copy-Item $_.FullName -Destination $targetFrames }
        Write-Host " $($jpgs.Count) frame images" -ForegroundColor Green
    }
} else {
    Write-Host " WARNING: storyboard-frames/ not found, skipping" -ForegroundColor Yellow
}

# ── 5. Create index redirect ────────────────────────────────────
Write-Host "[5/5] Creating index redirect ..." -NoNewline
@"
<!DOCTYPE html>
<html>
<head>
  <meta http-equiv="refresh" content="0; url=f01_bubble_studio.html" />
  <title>Circle the Square</title>
</head>
<body>
  <p>Redirecting to <a href="f01_bubble_studio.html">f01_bubble_studio.html</a>...</p>
</body>
</html>
"@ | Out-File -FilePath (Join-Path $DocsDir "index.html") -Encoding utf8
Write-Host " done" -ForegroundColor Green

# ── Summary ─────────────────────────────────────────────────────
Write-Host ""
Write-Host "Deploy contents:" -ForegroundColor Cyan
Get-ChildItem $DocsDir -Recurse | ForEach-Object {
    $rel = $_.FullName.Replace($DocsDir + "\", "")
    $size = if (-not $_.PSIsContainer) { "$([Math]::Round($_.Length / 1KB, 1)) KB" } else { "<DIR>" }
    Write-Host "  $rel  ($size)"
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Commit docs/ to git and push:"
Write-Host "       git add docs/"
Write-Host "       git commit -m 'Deploy to GitHub Pages'"
Write-Host "       git push"
Write-Host ""
Write-Host "  2. Enable GitHub Pages in your repo:"
Write-Host "       Settings → Pages → Source: Deploy from branch"
Write-Host "       Branch: main /docs"
Write-Host ""
Write-Host "  3. Your viewer will be live at:"
Write-Host "       https://pcturtle69uplandme.github.io/circle_the_square/" -ForegroundColor Green
