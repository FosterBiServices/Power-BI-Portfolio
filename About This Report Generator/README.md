# About This Report AI Context Generator V1.3

This standalone PySide6 application analyzes a PBIP project locally, generates a structured context package and a robust AI prompt, validates the returned AI JSON against the actual model, and creates a single-column HTML DAX measure.

The application does not call an external AI service and does not upload model metadata. Copy the generated prompt into your approved AI tool, then paste the JSON response back into this application.

## Download

**[AboutThisReportGenerator.exe](https://github.com/FosterBiServices/Power-BI-Portfolio/releases/latest/download/AboutThisReportGenerator.exe)**: a single-file Windows app with no install or Python needed. See [Releases](https://github.com/FosterBiServices/Power-BI-Portfolio/releases) for all versions.

> The app is not code-signed, so Windows may show *"Windows protected your PC"* on first run. Select **More info → Run anyway**.

## Run from source (Anaconda)

```cmd
cd /d "<repo>\About This Report Generator"
python -m pip install -e .
python -m about_report_generator
```

## Build the .exe

```powershell
cd "<repo>\About This Report Generator"
powershell -ExecutionPolicy Bypass -File .\build_exe.ps1 -Python "$env:USERPROFILE\anaconda3\python.exe"
```

Creates `dist\AboutThisReportGenerator.exe` using an isolated `.venv` (PySide6 + PyInstaller).

## Workflow

1. Open PBIP.
2. Review Context JSON.
3. Copy AI Prompt.
4. Submit prompt to your approved AI tool.
5. Paste the JSON-only response into AI Response JSON, or load a `.json` file.
6. Select Build DAX.
7. Copy or save the generated measure.

## Output sections

- Report Summary
- Data Sources
- Business Value
- Top KPIs

Technical model details and relationship strategy are not included in the HTML output.
