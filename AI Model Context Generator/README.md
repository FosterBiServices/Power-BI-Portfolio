# Semantic Model Context Builder

A local Python application that reads a Power BI PBIP file and writes one AI-readable semantic model context file.

## Download

**[AIModelContextGenerator.exe](https://github.com/FosterBiServices/Power-BI-Portfolio/releases/latest/download/AIModelContextGenerator.exe)**: a single-file Windows app (the desktop interface) with no install or Python needed. See [Releases](https://github.com/FosterBiServices/Power-BI-Portfolio/releases) for all versions.

> The app is not code-signed, so Windows may show *"Windows protected your PC"* on first run. Select **More info → Run anyway**.

## Scope

- Select an actual `.pbip` file.
- Resolve the referenced report and semantic model paths.
- Read TMDL table, column, measure, and relationship metadata, including `///` descriptions.
- Detect each table's data source (SQL Server, Excel, Quickbase, SharePoint, Lakehouse, DAX calculated tables, and more), following staging-query references to the real connector.
- Apply privacy controls before export. Source locations are included only when requested.
- Validate relationship endpoints, duplicate names, and DAX (syntax errors and references to objects that don't exist).
- Write one `.semantic-context.md` file.
- Support both a PySide6 desktop interface and a CLI.

## Run from source (Anaconda)

```powershell
cd "<repo>\AI Model Context Generator"
pip install "PySide6>=6.7,<6.10"
python -m semantic_model_context
```

or the command-line interface:

```powershell
python -m semantic_model_context.cli build "C:\Projects\Sales\Sales.pbip" --output "C:\Temp\Sales.semantic-context.md"
```

Options: `--include-hidden`, `--exclude-dax`, `--include-source-locations`.

Or install it (`pip install -e .`) to get the `semantic-context` and `semantic-context-gui` commands.

## Build the .exe

```powershell
cd "<repo>\AI Model Context Generator"
powershell -ExecutionPolicy Bypass -File .\build_exe.ps1 -Python "$env:USERPROFILE\anaconda3\python.exe"
```

Creates `dist\AIModelContextGenerator.exe` using an isolated `.venv` (PySide6 + PyInstaller). Settings and logs are stored in `%APPDATA%\SemanticModelContextBuilder`.

## Validate

```powershell
pytest
ruff check .
mypy semantic_model_context
```

## Design

The UI and CLI call the same `ContextService`. PBIP resolution, parsing, validation, privacy filtering, and Markdown output are separate modules so the parser can later be shared with Local TMDL Documenter.
