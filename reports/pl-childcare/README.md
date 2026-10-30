[← All reports](../README.md)

# PL Childcare

A child care subsidy payments report for a state workforce board. It reconciles provider payments between two systems, tracks spending against the fiscal-year budget and audits mismatches by region and county.

**File:** [`PL Childcare.pbix`](./PL%20Childcare.pbix)

## About the data

Everything in this report is **fictional**. It was rebuilt as a portfolio sample from a production report, with:

- all records replaced by **synthetic data** generated to keep realistic volumes, distributions and relationships, but no real people, clients, amounts or identifiers;
- the organisation rebranded as **Midwest Workforce Partnership (MWP)**, a made-up company, with its own logo;
- the state renamed **Prairieland (PL)**, with fictional regions (e.g. Cottonwood, Red Cedar), counties, cities and child care providers;
- system and vendor names generalised (for example *ERP*, *HRIS*, *ATS*, *LMS*, *the program database*).

Any resemblance to real people or organisations is coincidental.

## Report pages

| Page | What it shows |
|---|---|
| Summary | Paid amounts, households and children served, monthly budget and payments to date, by fund type, eligibility designation and county/city. |
| Audit | Records that don't match between the payment system (245) and the matrix extract, for reconciliation. |
| About This Report | Report notes and definitions. |
| Details / Provider Details (drill-through) | Hidden pages reached from the summary for payment- and provider-level detail. |

## Model at a glance

| | |
|---|---|
| Tables | 18 |
| Measures | 71 |
| Relationships | 21 |
| Calculation groups | 1 |
| DAX user-defined functions | 1 (trend helper) |
| Row-level security roles | 5 (one per region) |

## Techniques worth a look

- **Two-system reconciliation:** the payment file and matrix file are compared row by row, and mismatches surface on the Audit page.
- **Row-level security** by region.
- **Dynamic axis / field-parameter selectors** so one visual can switch between dimensions.
- **HTML Content visuals** for KPI cards, plus a personalised welcome line built from the signed-in user's name.
- **History tables** kept alongside the current extracts for month-over-month comparisons.

## Opening the report

1. Download **`PL Childcare.pbix`** from this folder.
2. Open it in a recent version of **Power BI Desktop** (Windows). This model uses **DAX user-defined functions**, so an older Desktop version may not open it.
3. The data is already imported, so every page works without refreshing.

Refreshing needs access to the original SharePoint source folders, so **Refresh** will fail outside that environment. That's expected; the sample data travels with the file.
