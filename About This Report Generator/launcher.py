# PyInstaller entry point: imports the package so its relative imports resolve inside the frozen app.
from about_report_generator.app import main

raise SystemExit(main())
