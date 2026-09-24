# Builds a single-file, windowed ModelDocumenter.exe into .\dist
# Usage:  .\build_exe.ps1                      (uses "python" on PATH)
#         .\build_exe.ps1 -Python C:\Users\<you>\anaconda3\python.exe

param(
  [string]$Python = "python"
)

$ErrorActionPreference = "Stop"

# Runs a native command and fails on a non-zero exit code. Native tools (pip, PyInstaller) write
# progress to stderr, which Windows PowerShell 5.1 would otherwise treat as a terminating error.
function Invoke-Native {
  param([string]$Exe, [string[]]$Arguments)
  $previous = $ErrorActionPreference
  $ErrorActionPreference = "Continue"
  try { & $Exe @Arguments 2>&1 | ForEach-Object { "$_" } }
  finally { $ErrorActionPreference = $previous }
  if ($LASTEXITCODE -ne 0) { throw "'$Exe $($Arguments -join ' ')' failed with exit code $LASTEXITCODE" }
}

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

if (-not (Test-Path ".\local_tmdl_documenter\app.py")) {
  throw "local_tmdl_documenter\app.py was not found. Run this script from the project root."
}
if (-not (Get-Command $Python -ErrorAction SilentlyContinue)) {
  throw "Python was not found ('$Python'). Pass -Python with the full path to python.exe (for example your Anaconda python.exe)."
}

# Isolated build environment keeps the exe small (Anaconda base would pull in unrelated libraries)
$Venv = Join-Path $ProjectRoot ".venv"
if (-not (Test-Path "$Venv\Scripts\python.exe")) {
  Invoke-Native $Python @("-m", "venv", $Venv)
}
$VenvPython = "$Venv\Scripts\python.exe"

Invoke-Native $VenvPython @("-m", "pip", "install", "--upgrade", "pip")
Invoke-Native $VenvPython @("-m", "pip", "install", "-r", "requirements.txt", "pyinstaller")

$Version = (& $VenvPython -c "import local_tmdl_documenter as m; print(m.__version__)").Trim()

# --specpath keeps the generated .spec inside build\ so it doesn't clutter the repo
Invoke-Native $VenvPython @(
  "-m", "PyInstaller",
  "--noconfirm", "--clean",
  "--onefile", "--windowed",
  "--name", "ModelDocumenter",
  "--specpath", "build",
  "--exclude-module", "tkinter",
  "launcher.py"
)

$ExePath = Join-Path $ProjectRoot "dist\ModelDocumenter.exe"
if (-not (Test-Path $ExePath)) {
  throw "Build completed without the expected executable: $ExePath"
}

$SizeMb = [math]::Round((Get-Item $ExePath).Length / 1MB, 1)
Write-Host ""
Write-Host "Model Documenter v$Version built ($SizeMb MB):" -ForegroundColor Green
Write-Host $ExePath
Write-Host "Single file - share ModelDocumenter.exe on its own."
