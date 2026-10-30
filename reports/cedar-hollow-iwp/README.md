[← All reports](../README.md)

# CEDAR HOLLOW - IWP

An operations report for a county interim housing (hotel-based) program. It covers activations, client demographics, room nights, staffing, financials, call-centre activity and data-quality checks across the program's systems.

**File:** [`CEDAR HOLLOW - IWP.pbix`](./CEDAR%20HOLLOW%20-%20IWP.pbix)

## About the data

Everything in this report is **fictional**. It was rebuilt as a portfolio sample from a production report, with:

- all records replaced by **synthetic data** generated to keep realistic volumes, distributions and relationships, but no real people, clients, amounts or identifiers;
- the organisation rebranded as **Midwest Workforce Partnership (MWP)**, a made-up company, with its own logo;
- the county renamed **Cedar Hollow County** in the fictional state of **Lakeshore**, with invented service areas, communities, hotels and ZIP codes;
- system and vendor names generalised (for example *ERP*, *HRIS*, *ATS*, *LMS*, *the program database*).

Any resemblance to real people or organisations is coincidental.

## Report pages

| Page | What it shows |
|---|---|
| Program Overview | Activations, clients, rooms, average length of stay, gender, race/ethnicity and household composition. |
| Staff | Staffing and staff-time measures. |
| Search | Look up a client or record across sources. |
| Financials | Monthly actuals vs budget by fund. |
| Call Activity | Call volumes and patterns, including flags for possible line misuse. |
| Data Integrity | Cross-system checks: duplicate IDs, mismatched names, records found in only one system, census variance. |
| Hidden drill-down pages | Demographics variance, multiple communities, census variance, HMIS-only/MPR-only records, name mismatches and staff-time review. |

## Model at a glance

| | |
|---|---|
| Tables | 29 |
| Measures | 131 |
| Relationships | 21 |

## Techniques worth a look

- **Data-quality reporting:** the program's monthly report (MPR) is compared with the HMIS export and the intake log to flag duplicates, name mismatches and records missing from either side.
- **Measure-selection tables** that let one visual switch between people, capacity and staff measures.
- **Search page** built on text slicers for record lookup.
- **Page navigator buttons and drill-down pages** for moving from summary to detail.

## Opening the report

1. Download **`CEDAR HOLLOW - IWP.pbix`** from this folder.
2. Open it in a recent version of **Power BI Desktop** (Windows).
3. The data is already imported, so every page works without refreshing.

Refreshing needs access to the original SharePoint source folders, so **Refresh** will fail outside that environment. That's expected; the sample data travels with the file.
