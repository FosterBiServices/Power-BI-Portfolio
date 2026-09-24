# Model Documenter

A local PySide6 application that reads PBIP/TMDL and PBIR files in place and generates a standalone HTML documentation report.

## Run with Anaconda

```powershell
cd C:\Projects\LocalTmdlDocumenter
pip install -r requirements.txt
python -m local_tmdl_documenter
```

Select the PBIP project folder, `.SemanticModel` folder, or semantic model `definition` folder. For report-page documentation, select the common PBIP parent containing both `.SemanticModel` and `.Report` folders.

## Privacy

- No network calls or telemetry.
- Source files are read in place and are never copied.
- Documentation is written only when you select an output path.
- DAX, Power Query, source paths, and hidden objects are opt-in.
- Credentials and common connection secrets are redacted from generated HTML.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
