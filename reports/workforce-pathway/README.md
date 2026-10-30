[← All reports](../README.md)

# Workforce Pathway

Product analytics for a mobile career-coaching app used by workforce programs. It follows members from enrollment through engagement, learning content, job readiness (résumés) and self-assessments, alongside coach caseloads.

**File:** [`Workforce Pathway.pbix`](./Workforce%20Pathway.pbix)

## About the data

Everything in this report is **fictional**. It was rebuilt as a portfolio sample from a production report, with:

- all records replaced by **synthetic data** generated to keep realistic volumes, distributions and relationships, but no real people, clients, amounts or identifiers;
- the organisation rebranded as **Midwest Workforce Partnership (MWP)**, a made-up company, with its own logo;
- program names generalised (e.g. *South Bluestem*) and all members, coaches and content titles invented;
- system and vendor names generalised (for example *ERP*, *HRIS*, *ATS*, *LMS*, *the program database*).

Any resemblance to real people or organisations is coincidental.

## Report pages

| Page | What it shows |
|---|---|
| Program Overview | KPI cards for new enrollments, active members, resources completed and résumés created, an engagement funnel and members by program. |
| Trends | Enrollments vs the same month last year, weekly active members, resources completed and résumés by month. |
| Coach Caseload | Caseload per coach, members who need a nudge, upcoming appointments. |
| Member Detail | One member's timeline, completed resources and assessments. |
| Member Engagement | Sessions, active days, activity by type, hour and day of week. |
| Learning & Content | Content viewed vs completed, minutes of learning. |
| Job Readiness | Résumés created, exported and tailored; profile updates. |
| Assessments | Self-assessment and career-interest results. |
| About this Report | Definitions. |

## Model at a glance

| | |
|---|---|
| Tables | 62 (built from about 30 raw app-export CSVs) |
| Measures | 232 |
| Relationships | 59 |
| DAX user-defined functions | 11 (HTML/SVG card and tile builders, paging and trend helpers) |

## Techniques worth a look

- **KPI cards drawn in DAX:** 11 user-defined functions return HTML and inline SVG for the HTML Content visual, with monthly columns, month-over-month pills and hover tooltips. About 40 cards share the same functions.
- **Swappable source:** a `SourceType` parameter switches every table between SharePoint CSV exports and a Databricks SQL warehouse; here the SharePoint path is used.
- **Paging tables** for long lists (coaches, members, resources) with rows-per-page and page-number slicers.
- **Bridge tables** expand the app's comma-separated relationship fields (topics, sub-topics, resources, assessments) into proper many-to-many links.

## Opening the report

1. Download **`Workforce Pathway.pbix`** from this folder.
2. Open it in a recent version of **Power BI Desktop** (Windows). This model uses **DAX user-defined functions**, so an older Desktop version may not open it.
3. The data is already imported, so every page works without refreshing.

Refreshing needs access to the original SharePoint source folders, so **Refresh** will fail outside that environment. That's expected; the sample data travels with the file.
