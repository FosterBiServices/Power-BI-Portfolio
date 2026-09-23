# Semantic Model Context Builder

Version 1.0 project scaffold for a local Python application that reads a Power BI PBIP file and writes one AI-readable semantic model context file.

## Version 1.0 scope

- Select an actual `.pbip` file.
- Resolve the referenced report and semantic model paths.
- Read TMDL table, column, measure, and relationship metadata.
- Apply privacy controls before export.
- Validate relationship endpoints and duplicate object names.
- Write one `.semantic-context.md` file.
- Support both a PySide6 desktop interface and a CLI.

## Install for development

```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

## Run

```powershell
semantic-context-gui
```

or:

```powershell
semantic-context build "C:\Projects\WeCARE\WeCARE.pbip"
```

## Validate

```powershell
pytest
ruff check .
mypy src
```

## Design

The UI and CLI call the same `ContextService`. PBIP resolution, parsing, validation, privacy filtering, and Markdown output are separate modules so the parser can later be shared with Local TMDL Documenter.
