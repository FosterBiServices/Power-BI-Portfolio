# PyInstaller entry point: imports the package so its relative imports resolve inside the frozen app.
from semantic_model_context.app import main

raise SystemExit(main())
