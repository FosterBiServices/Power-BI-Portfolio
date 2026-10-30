# Tools

Small Python utilities I built to speed up Power BI development.

| Tool | What it does |
|---|---|
| [`dax-html-generator/`](dax-html-generator/) | Reads a metric-threshold workbook and **generates DAX measures that render HTML scorecards** (RAG thresholds, YTD and YoY flags, comment panels) for each program type. Sample output is in `final-output/`. |
| [`pbip-helpers/`](pbip-helpers/) | PBIP maintenance: remove duplicate lineage tags, convert TMDL to plain text for Copilot, and build the [`dax/`](../dax/) pattern and UDF folders in this repo. |
| [`theme-generator/`](theme-generator/) | Build a complete Power BI theme JSON from one template and a colour palette. |

The notebooks run in Jupyter or VS Code with Python 3. Paths use placeholders such as `C:\Users\<USER>\...`; set them before running.
