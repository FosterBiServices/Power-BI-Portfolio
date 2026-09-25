// Date Table - Dynamic Filters
// Ways to limit a date table (or any table with a date column) to a moving window,
// so the model stays small and slicers only show relevant dates.
// Paste the step(s) you need; <DATE_TABLE> is your date table query and
// [<DATE_COLUMN>] its date column. Filters on a SQL source fold to the WHERE clause.
//
// Tip: Date.From(DateTime.LocalNow()) is "today" on your PC, but UTC in the Power BI
// service. Use Date.From(fxUtcToEastern(DateTimeZone.UtcNow())) where the boundary matters.


// =====================================================================
// 1) Rolling window: up to (but not including) today, last N days
// =====================================================================
let
    Source       = <DATE_TABLE>,
    Today        = Date.From(DateTime.LocalNow()),
    DaysBack     = 730,                                           // ~2 years
    RollingDates = Table.SelectRows(
        Source,
        each [<DATE_COLUMN>] < Today and [<DATE_COLUMN>] >= Date.AddDays(Today, -DaysBack)
    )
in
    RollingDates


// =====================================================================
// 2) Year range relative to today (e.g. 4 years back through next year)
// ---------------------------------------------------------------------
// Works on a calendar or fiscal year number column.
// =====================================================================
let
    Source      = <DATE_TABLE>,
    CurrentYear = Date.Year(Date.From(DateTime.LocalNow())),
    YearRange   = Table.SelectRows(
        Source,
        each [<YEAR_COLUMN>] >= CurrentYear - 4 and [<YEAR_COLUMN>] <= CurrentYear + 1
    )
in
    YearRange


// =====================================================================
// 3) Current and previous (fiscal) year using flag columns from the source
// ---------------------------------------------------------------------
// Many warehouse date views ship IsCurrent... / IsPrevious... flags.
// Select, type and rename them into friendly names in one pass.
// =====================================================================
let
    Source = <DATE_TABLE>,

    KeptColumns = Table.SelectColumns(
        Source,
        {"<DATE_COLUMN>", "<YEAR_COLUMN>", "<PERIOD_COLUMN>", "<IS_CURRENT_YEAR_FLAG>", "<IS_PREVIOUS_YEAR_FLAG>"}
    ),
    Typed   = Table.TransformColumnTypes(KeptColumns, {{"<DATE_COLUMN>", type date}}),
    Renamed = Table.RenameColumns(
        Typed,
        {
            {"<DATE_COLUMN>", "Date"},
            {"<YEAR_COLUMN>", "Fiscal Year"},
            {"<PERIOD_COLUMN>", "Fiscal Period"},
            {"<IS_CURRENT_YEAR_FLAG>", "Current Year"},
            {"<IS_PREVIOUS_YEAR_FLAG>", "Previous Year"}
        }
    ),
    UpToToday      = Table.SelectRows(Renamed, each [Date] < Date.From(DateTime.LocalNow())),
    CurrentAndPrev = Table.SelectRows(UpToToday, each [Current Year] = true or [Previous Year] = true)
in
    CurrentAndPrev


// =====================================================================
// 4) Match the date table to the data: min/max of fact table(s)
// ---------------------------------------------------------------------
// Keeps the date table from running years past the last row of data.
// With two facts (e.g. a start event and an end event) take the earliest start
// and the latest end.
// =====================================================================
let
    Source  = <DATE_TABLE>,
    MinDate = List.Min(<FACT_TABLE>[<DATE_COLUMN>]),
    MaxDate = List.Max(<FACT_TABLE_2>[<DATE_COLUMN>]),

    // Whole years avoid partial-year problems in time intelligence
    WholeYears = Table.SelectRows(
        Source,
        each [<DATE_COLUMN>] >= Date.StartOfYear(MinDate) and [<DATE_COLUMN>] <= Date.EndOfYear(MaxDate)
    )
in
    WholeYears


// =====================================================================
// 5) Last complete week (Monday - Sunday)
// ---------------------------------------------------------------------
// For a Sunday-Saturday week, use Day.Sunday instead of Day.Monday.
// =====================================================================
let
    Source        = <TABLE>,
    Today         = Date.From(DateTime.LocalNow()),
    ThisWeekStart = Date.StartOfWeek(Today, Day.Monday),
    LastWeekStart = Date.AddDays(ThisWeekStart, -7),
    LastWeek      = Table.SelectRows(
        Source,
        each [<DATE_COLUMN>] >= LastWeekStart and [<DATE_COLUMN>] < ThisWeekStart
    )
in
    LastWeek
