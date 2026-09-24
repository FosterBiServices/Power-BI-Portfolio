$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

if (-not (Test-Path ".\local_tmdl_documenter\app.py")) {
  throw "local_tmdl_documenter\app.py was not found. Run this script from the project root."
}

$PythonCommand = Get-Command python -ErrorAction SilentlyContinue
if (-not $PythonCommand) {
  throw "Python was not found on PATH. Install standard Python or run from an environment that provides python.exe."
}

python -m pip install --upgrade pip
python -m pip install -r requirements.txt pyinstaller

@'
from local_tmdl_documenter.app import main

raise SystemExit(main())
'@ | Set-Content -Path ".\launcher.py" -Encoding UTF8

python -m PyInstaller --noconfirm --clean ".\LocalTmdlDocumenter.spec"

$ExePath = Join-Path $ProjectRoot "dist\LocalTmdlDocumenter\LocalTmdlDocumenter.exe"
if (-not (Test-Path $ExePath)) {
  throw "Build completed without the expected executable: $ExePath"
}

Write-Host ""
Write-Host "Standalone application created:" -ForegroundColor Green
Write-Host $ExePath
Write-Host ""
Write-Host "Copy the entire dist\LocalTmdlDocumenter folder when distributing the application."
