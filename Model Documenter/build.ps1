$ErrorActionPreference = "Stop"
python -m pip install -r requirements.txt pyinstaller
python -m PyInstaller --noconfirm --clean --windowed --name LocalTmdlDocumenterV2 --collect-all PySide6 -m local_tmdl_documenter
Write-Host "Built: dist\LocalTmdlDocumenterV2\LocalTmdlDocumenterV2.exe"
