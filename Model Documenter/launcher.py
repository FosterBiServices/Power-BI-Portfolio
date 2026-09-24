# PyInstaller entry point: imports the package so its relative imports resolve inside the frozen app.
from local_tmdl_documenter.app import main

raise SystemExit(main())
