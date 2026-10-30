# Steven Foster · Power BI Portfolio

**Analytics engineer and Power BI developer** with 9+ years turning data into decisions across retail, healthcare and workforce services. This repository holds sample reports rebuilt from production work, plus the DAX, Power Query, Tabular Editor and AI tooling I use to build them.

`Power BI` · `DAX` · `DAX UDFs` · `Power Query (M)` · `PBIP / TMDL / PBIR` · `Tabular Editor` · `Semantic modelling` · `Row-level security` · `SVG & HTML visuals in DAX`

---

## Featured reports

Production reports rebuilt as samples. Every record is **synthetic** and the client is rebranded as the fictional **Midwest Workforce Partnership**, while the original design, model and DAX are kept. Download a `.pbix` and open it in Power BI Desktop; no refresh or login is needed.

| Report | Highlights |
|---|---|
| [**MWP US Project Scorecard**](reports/mwp-us-project-scorecard/) | Executive risk scorecard over 85 tables and 526 measures. Configurable weighted scoring, and data from five systems (program database, ERP, HRIS, ATS, LMS) in one model. |
| [**Workforce Pathway**](reports/workforce-pathway/) | Product analytics for a career-coaching app. About 40 KPI cards drawn in HTML and SVG by 11 DAX user-defined functions, with hover tooltips. |
| [**DVR LJC Collaboration**](reports/dvr-ljc-collaboration/) | Multi-agency grant reporting. A single `ApplyPeriod` UDF switches 17 measures between monthly and cumulative views, and colour-helper UDFs format survey results. |
| [**PL Childcare**](reports/pl-childcare/) | Subsidy payments reconciled across two systems, budget vs actual, and row-level security by region. |
| [**Cedar Hollow IWP**](reports/cedar-hollow-iwp/) | Interim housing operations with cross-system data-quality checks (duplicates, name mismatches, census variance). |
| [**Power BI Résumé**](reports/power-bi-resume/) | My résumé as an interactive report. |

## Repository map

```
reports/          Sample .pbix files, each with a README (pages, model, techniques)
dax/
  udf-library/    Versioned DAX user-defined function library (time intelligence)
  time-intelligence/  Classic measure templates: YTD, PY, MoM, YoY, MAT, ...
  patterns/       SVG KPI cards & icons, conditional formatting, navigation, security
power-query/      Reusable M functions and patterns: ingestion, cleansing, dates
tabular-editor/   C# scripts: model hygiene, measure generation, documentation
ai-skills/        Agent skills that add advanced visuals to PBIP projects
tools/            Python helpers: DAX/HTML generator, theme generator, PBIP utilities
about/            Résumé and certifications
```

## How I work

- **Source-controlled models:** projects are developed as **PBIP** (TMDL + PBIR), so every measure, query and visual change can be reviewed in Git.
- **Reuse over repetition:** DAX user-defined functions, calculation groups and Power Query functions replace copy-pasted logic.
- **Automation:** Tabular Editor scripts and Python handle formatting, documentation and bulk measure creation.
- **Design in the model:** SVG and HTML measures produce KPI cards and visuals that core Power BI visuals can't.

## About the sample data

The sample reports contain no real people, clients, amounts or identifiers. Data was generated to resemble production volumes and distributions, place names were replaced with fictional ones, and vendor systems are named generically (ERP, HRIS, ATS, LMS).

## Contact

Steven Foster · Foster BI Services · fosterbiservices@gmail.com
