# Model Documenter

A local PySide6 application that reads PBIP/TMDL and PBIR files in place and generates a standalone HTML documentation report.

## Download

**[ModelDocumenter.exe](https://github.com/FosterBiServices/Power-BI-Portfolio/releases/latest/download/ModelDocumenter.exe)**: a single-file Windows app with no install or Python needed. See [Releases](https://github.com/FosterBiServices/Power-BI-Portfolio/releases) for all versions.

> The app is not code-signed, so Windows may show *"Windows protected your PC"* on first run. Select **More info → Run anyway**.

## Use

Select the PBIP project folder, `.SemanticModel` folder, or semantic model `definition` folder. For report-page documentation, select the common PBIP parent containing both `.SemanticModel` and `.Report` folders.

## Privacy

- No network calls or telemetry.
- Source files are read in place and are never copied.
- Documentation is written only when you select an output path.
- DAX, Power Query, source paths, and hidden objects are opt-in.
- Credentials and common connection secrets are redacted from generated HTML.

## Run from source (Anaconda)

```powershell
cd "<repo>\Model Documenter"
pip install -r requirements.txt
python -m local_tmdl_documenter
```

## Build the .exe

```powershell
cd "<repo>\Model Documenter"
powershell -ExecutionPolicy Bypass -File .\build_exe.ps1 -Python "$env:USERPROFILE\anaconda3\python.exe"
```

Creates `dist\ModelDocumenter.exe` using an isolated `.venv` (PySide6 + PyInstaller). Settings and logs are stored in `%APPDATA%\LocalTmdlDocumenter`.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
