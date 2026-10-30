[← All reports](../README.md)

# DVR LJC Collaboration

A grant-collaboration report between a state vocational rehabilitation agency (DVR) and its local job centers (LJC). It tracks enrollments, services, exits to employment, and partner readiness and partnership surveys across workforce board regions.

**File:** [`DVR LJC Collaboration.pbix`](./DVR%20LJC%20Collaboration.pbix)

## About the data

Everything in this report is **fictional**. It was rebuilt as a portfolio sample from a production report, with:

- all records replaced by **synthetic data** generated to keep realistic volumes, distributions and relationships, but no real people, clients, amounts or identifiers;
- the organisation rebranded as **Midwest Workforce Partnership (MWP)**, a made-up company, with its own logo;
- the state renamed **Lakeshore**, with fictional workforce board regions, districts and partner sites;
- system and vendor names generalised (for example *ERP*, *HRIS*, *ATS*, *LMS*, *the program database*).

Any resemblance to real people or organisations is coincidental.

## Report pages

| Page | What it shows |
|---|---|
| Grant Enrollment | Enrollment by region against targets, with a Monthly / Total toggle. |
| Service Utilization | Which services are provided and how much, by category. |
| Exiters by Region | Participants exiting, and exits with employment. |
| Localized Contributions | Region-level contribution to the grant goals. |
| Project Readiness Baseline | Partner-site readiness survey results by item. |
| Operational Needs Assessment | Alignment, process and training needs from the assessment survey. |
| DVR Staff Survey | Staff perceptions of the collaboration, item by item. |
| Partnership Reflection | End-of-period partnership reflection survey. |
| Accomplishments & Lessons Learned | Narrative responses. |
| Tooltip and detail pages | Hidden pages for hover tooltips and question-level detail. |

## Model at a glance

| | |
|---|---|
| Tables | 21 |
| Measures | 207 |
| Relationships | 12 |
| DAX user-defined functions | 5 (`ApplyPeriod` plus survey colour helpers) |

## Techniques worth a look

- **`ApplyPeriod` UDF:** one function switches about 17 measures between cumulative and single-month values from a slicer, instead of duplicating logic in every measure.
- **Colour-helper UDFs** apply consistent conditional formatting to survey responses (agreement scales, impact scales, 1–10 ratings).
- **Field-parameter style selectors** for switching survey questions and Top-N regions.
- **Heavy use of tooltip pages** to show question-level detail on hover.

## Opening the report

1. Download **`DVR LJC Collaboration.pbix`** from this folder.
2. Open it in a recent version of **Power BI Desktop** (Windows). This model uses **DAX user-defined functions**, so an older Desktop version may not open it.
3. The data is already imported, so every page works without refreshing.

Refreshing needs access to the original SharePoint source folders, so **Refresh** will fail outside that environment. That's expected; the sample data travels with the file.
