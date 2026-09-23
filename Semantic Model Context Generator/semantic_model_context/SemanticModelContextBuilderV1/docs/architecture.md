# Architecture

```text
PySide6 GUI ─┐
             ├── ContextService
CLI ─────────┘       │
                     ├── PBIP Resolver
                     ├── TMDL Parser
                     ├── Privacy Filter
                     ├── Validator
                     └── Markdown Writer
```

## Integration point with Local TMDL Documenter

Move the existing PBIP/TMDL parsing code into `TmdlParser.parse`. Keep the domain conversion inside the parser boundary. The UI, CLI, privacy filter, validator, and writer must not read TMDL files directly.
