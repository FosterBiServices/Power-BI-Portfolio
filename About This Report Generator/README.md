# About This Report AI Context Generator V1.3

This standalone PySide6 application analyzes a PBIP project locally, generates a structured context package and a robust AI prompt, validates the returned AI JSON against the actual model, and creates a single-column HTML DAX measure.

The application does not call an external AI service and does not upload model metadata. Copy the generated prompt into your approved AI tool, then paste the JSON response back into this application.

## Launch through Anaconda

```cmd
cd /d "C:\Projects\About This Report Generator"
python -m pip install -e .
python -m about_report_generator
```

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
