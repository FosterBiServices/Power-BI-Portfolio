[← All reports](../README.md)

# MWP US Project Scorecard

An executive portfolio scorecard that rates every active workforce-services project on performance, finance, staffing and compliance risk, then rolls the results up by vice president and region.

**File:** [`MWP US Project Scorecard.pbix`](./MWP%20US%20Project%20Scorecard.pbix)

## About the data

Everything in this report is **fictional**. It was rebuilt as a portfolio sample from a production report, with:

- all records replaced by **synthetic data** generated to keep realistic volumes, distributions and relationships, but no real people, clients, amounts or identifiers;
- the organisation rebranded as **Midwest Workforce Partnership (MWP)**, a made-up company, with its own logo;
- real US state codes kept (the portfolio spans the country), with project, town and site names invented;
- system and vendor names generalised (for example *ERP*, *HRIS*, *ATS*, *LMS*, *the program database*).

Any resemblance to real people or organisations is coincidental.

## Report pages

| Page | What it shows |
|---|---|
| Risk Values | Every KPI for each project in one matrix, colour-coded red/amber/green against configurable thresholds. |
| Weighted Risk Scores | Each KPI converted to a score and weighted into a single project health score, with 1- and 3-month change. |
| Ranking by Measure | Projects ranked on any KPI chosen from a selector, top or bottom N. |
| MPR VP | Monthly performance review for a vice president's portfolio: projects, performance, expenditure trend and profit-tied measures. |
| MPR | Single-project monthly review: contract details, total risk score trend, fund-level budget vs spend, revenue and EBITDA vs budget, monitoring and staffing. |
| Performance Snapshot | Company-wide view of performance, expenditure, revenue/EBITDA and people & culture. |
| Regional Performance Overview / Regional Overview | The same story at regional level. |
| About this Report | Definitions for every KPI. |

## Model at a glance

| | |
|---|---|
| Tables | 85 (imported from about 60 source files) |
| Measures | 526 |
| Relationships | 81 |
| Calculation groups | 1 (snapshot period) |
| DAX user-defined functions | 6 (trend, variance and MOR formatting helpers) |

## Techniques worth a look

- **Configurable scoring:** thresholds, weights and RAG colours live in small *Enter Data* tables (`Thresholds`, `WeightedScoring`, `RAGFormatting`), so the scoring rules change without touching DAX.
- **Combining several systems:** program database (deliverables, outcomes, contracts, monitoring), ERP general ledger and budgets, HRIS headcount and turnover, ATS recruiting and LMS training, joined through location and profit-centre crosswalks.
- **Reusable DAX UDFs** for trailing-month trends and good/bad conditional formatting.
- **Fiscal-year time intelligence** (July–June), with month and quarter slicers driving disconnected trend tables.
- **SVG image measures** for card graphics, plus tooltip pages for drill-in detail.

## Opening the report

1. Download **`MWP US Project Scorecard.pbix`** from this folder.
2. Open it in a recent version of **Power BI Desktop** (Windows). This model uses **DAX user-defined functions**, so an older Desktop version may not open it.
3. The data is already imported, so every page works without refreshing.

Refreshing needs access to the original SharePoint source folders, so **Refresh** will fail outside that environment. That's expected; the sample data travels with the file.
