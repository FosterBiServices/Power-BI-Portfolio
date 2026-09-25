# Power Query (M) Patterns

Reusable Power Query patterns and custom functions. They're written as templates
to adapt, not as steps copied from a specific report.

## How to use

- **Functions** (`Functions/fx*.pq`) are complete queries. Create a blank query
  (Home > New Source > Blank Query), open the Advanced Editor, paste the file, and name
  the query after the file (e.g. `fxSetColumnTypes`). Usage examples are in each file's header.
- **Pattern files** (everything else) are one of two kinds:
  - a full `let ... in` query you can paste as-is, or
  - a set of steps to paste into an existing query. These start at `<PREVIOUS_STEP>`.
  Files with several `let ... in` blocks hold alternative versions. Copy the one you need.
- Files are plain text saved as `.pq`, the standard Power Query extension (VS Code's
  Power Query extension highlights it).

### Placeholders

Replace every `<...>` token before running:

| Placeholder | Meaning |
|---|---|
| `<TABLE>`, `<TABLE_2>` | a query/table name |
| `<FACT_TABLE>`, `<DATE_TABLE>`, `<LOOKUP_TABLE>`, `<HOLIDAY_TABLE>` | a table in that role |
| `<COLUMN>`, `<COLUMN_1>`, `<COLUMN_2>`, ... | a column name |
| `<DATE_COLUMN>`, `<KEY_COLUMN>`, `<GROUP_COLUMN>`, `<VALUE_COLUMN>`, ... | a column in that role |
| `<PREVIOUS_STEP>` | the step name the snippet builds on |
| `<SERVER>`, `<DATABASE>`, `<SCHEMA>` | SQL connection details (keep them in parameters) |
| `<SITE_URL>`, `<FOLDER_URL>`, `<FILE_URL>`, `<SHEET>` | SharePoint / Excel locations |
| `<VALUE>`, `<NEW_...>`, `<OLD_...>` | literal values to search for or rename to |

Inside `[...]` field access, e.g. `[<COLUMN>]`, use `[#"My Column"]` if the name
has special characters.

## Contents

### Functions
| File | What it does |
|---|---|
| [fxSetColumnTypes](Functions/fxSetColumnTypes.pq) | Explicit types for listed columns, default type for the rest, and no error when a column is missing |
| [fxInferColumnTypes](Functions/fxInferColumnTypes.pq) | Guess column types from the data (keeps leading-zero IDs as text) |
| [fxCleanColumnNames](Functions/fxCleanColumnNames.pq) | Trim names, replace underscores, apply Proper Case, strip a prefix |
| [fxSkipRowsUntilMarker](Functions/fxSkipRowsUntilMarker.pq) | Drop title rows above a marker row, then promote headers |
| [fxKeepRowsUntilMarker](Functions/fxKeepRowsUntilMarker.pq) | Drop footer/totals rows below a marker row |
| [fxReplaceErrorsInAllColumns](Functions/fxReplaceErrorsInAllColumns.pq) | Replace errors in every column at once |
| [fxExpandFirstRecordColumns](Functions/fxExpandFirstRecordColumns.pq) | Expand SharePoint person/lookup columns (list of records) in bulk |
| [fxAddValueCounts](Functions/fxAddValueCounts.pq) | Per-row counts of 0/1/2 (or any values) across question columns |
| [fxAddDateTimeFromPairs](Functions/fxAddDateTimeFromPairs.pq) | Split timestamps into date, time and yyyyMMdd key columns |
| [fxUtcToEastern](Functions/fxUtcToEastern.pq) | UTC to US Eastern with daylight saving time |
| [fxConvertColumnsUtcToEastern](Functions/fxConvertColumnsUtcToEastern.pq) | Apply fxUtcToEastern to several columns |
| [fxNetworkDays](Functions/fxNetworkDays.pq) | Working days between two dates (like Excel NETWORKDAYS) |
| [fxAddWorkdayFlag](Functions/fxAddWorkdayFlag.pq) | 1/0 working-day flag on a date table |

### Ingestion
| File | What it does |
|---|---|
| [SharePoint - Combine Excel Files from Folder](Ingestion/SharePoint%20-%20Combine%20Excel%20Files%20from%20Folder.pq) | Combine every workbook in a folder without helper queries |
| [Excel - Connect and Select Sheet](Ingestion/Excel%20-%20Connect%20and%20Select%20Sheet.pq) | Parameterized file path; pick a sheet by name, position, or keyword |
| [Database and Dataflow Sources](Ingestion/Database%20and%20Dataflow%20Sources.pq) | SQL with parameters, column pruning, same-source joins; dataflow entities |
| [Last Refresh Timestamp](Ingestion/Last%20Refresh%20Timestamp.pq) | "Data last refreshed" table in local time + DAX label |

### DataCleansing
| File | What it does |
|---|---|
| [Safe Column Operations](DataCleansing/Safe%20Column%20Operations.pq) | Remove/rename/select/transform columns without breaking on missing columns |
| [Row Validation Flags](DataCleansing/Row%20Validation%20Flags.pq) | "Reason Invalid" column and exceptions table for data-quality rules |
| [Replace Values from Mapping](DataCleansing/Replace%20Values%20from%20Mapping.pq) | Bulk replacements from a lookup table, record, or list of pairs |

### DateLogic
| File | What it does |
|---|---|
| [Date Table - Dynamic Filters](DateLogic/Date%20Table%20-%20Dynamic%20Filters.pq) | Rolling windows, relative year ranges, fit-to-data, last full week |
| [Date Table - Relative Columns](DateLogic/Date%20Table%20-%20Relative%20Columns.pq) | Current/previous week, "Current" month, months/days prior, fiscal year |
| [Holiday Table](DateLogic/Holiday%20Table.pq) | Generated US holiday table with observed dates |
| [Workday Calculations](DateLogic/Workday%20Calculations.pq) | Weekday counts per row, with holidays, prorated periods |
| [Merge Between Dates](DateLogic/Merge%20Between%20Dates.pq) | Join on key + date within an effective-date range |

### Transformations
| File | What it does |
|---|---|
| [Group and Aggregate](Transformations/Group%20and%20Aggregate.pq) | Latest-period filter, two-level grouping, safe ratio columns |
| [Previous Row Value by Group](Transformations/Previous%20Row%20Value%20by%20Group.pq) | LAG/LEAD within groups while keeping column types |
| [Name Formatting](Transformations/Name%20Formatting.pq) | "Last, First" for one or many name pairs; names from email; DAX UPN version |
| [Compare Tables](Transformations/Compare%20Tables.pq) | Added / removed / changed rows between two tables |
