// Date Table - Relative Columns
// Columns that describe each date relative to today (or to the last date with data).
// They recalculate on every refresh and make slicers like "Current Month" or
// "Last 3 Months" possible without DAX.
// Paste into a date table query; <PREVIOUS_STEP> is the step before and
// [<DATE_COLUMN>] the date column.


// =====================================================================
// Anchor dates (define once, near the top)
// =====================================================================
    Today = Date.From(DateTime.LocalNow()),

    // Last date that actually has data (use instead of Today for "as of" reporting)
    LastDateWithData = Date.From(List.Max(<FACT_TABLE>[<DATE_COLUMN>])),


// =====================================================================
// 1) Current / previous week flags (Sunday-start weeks; use Day.Monday for Monday-start)
// =====================================================================
    ThisWeekStart = Date.StartOfWeek(Today, Day.Sunday),

    AddCurrentWeek = Table.AddColumn(
        <PREVIOUS_STEP>,
        "Current Week",
        each if [<DATE_COLUMN>] >= ThisWeekStart and [<DATE_COLUMN>] <= Today then "Yes" else "No",
        type text
    ),

    AddPreviousWeek = Table.AddColumn(
        AddCurrentWeek,
        "Previous Week",
        each if [<DATE_COLUMN>] >= Date.AddDays(ThisWeekStart, -7) and [<DATE_COLUMN>] < ThisWeekStart then "Yes" else "No",
        type text
    ),


// =====================================================================
// 2) "Current" month label + numeric month sort
// ---------------------------------------------------------------------
// Month Filter shows "Current" for this month and the normal label otherwise,
// so a slicer default of "Current" keeps working month after month.
// Sort the label column by Month Sort (Column tools > Sort by column).
// =====================================================================
    AddMonthFilter = Table.AddColumn(
        AddPreviousWeek,
        "Month Filter",
        each
            if Date.Year([<DATE_COLUMN>]) = Date.Year(Today) and Date.Month([<DATE_COLUMN>]) = Date.Month(Today)
            then "Current"
            else Date.ToText([<DATE_COLUMN>], "MMM yyyy"),
        type text
    ),

    AddMonthSort = Table.AddColumn(
        AddMonthFilter,
        "Month Sort",
        each Date.Year([<DATE_COLUMN>]) * 12 + Date.Month([<DATE_COLUMN>]) - 1,
        Int64.Type
    ),


// =====================================================================
// 3) Offsets: months / days before the anchor date
// ---------------------------------------------------------------------
// 0 = anchor month/day, 1 = one before, -1 = one after.
// Filter with "Months Prior <= 2" for a rolling 3 months, etc.
// =====================================================================
    AnchorDate = LastDateWithData,        // or Today

    AddMonthsPrior = Table.AddColumn(
        AddMonthSort,
        "Months Prior",
        each (Date.Year(AnchorDate) - Date.Year([<DATE_COLUMN>])) * 12
            + (Date.Month(AnchorDate) - Date.Month([<DATE_COLUMN>])),
        Int64.Type
    ),

    AddDaysPrior = Table.AddColumn(
        AddMonthsPrior,
        "Days Prior",
        each Duration.Days(AnchorDate - Date.From([<DATE_COLUMN>])),
        Int64.Type
    ),

    // Marks the single anchor date, e.g. for a "Data through <date>" label
    AddLastDateFlag = Table.AddColumn(
        AddDaysPrior,
        "Is Last Date With Data",
        each Date.From([<DATE_COLUMN>]) = LastDateWithData,
        type logical
    ),


// =====================================================================
// 4) Fiscal year that starts in a month other than January
// =====================================================================
    FiscalYearStartMonth = 7,             // July; fiscal year named after the year it ends

    AddFiscalYear = Table.AddColumn(
        AddLastDateFlag,
        "Fiscal Year",
        each Date.Year([<DATE_COLUMN>]) + (if Date.Month([<DATE_COLUMN>]) >= FiscalYearStartMonth then 1 else 0),
        Int64.Type
    ),

    AddFiscalMonth = Table.AddColumn(
        AddFiscalYear,
        "Fiscal Month Number",
        each Number.Mod(Date.Month([<DATE_COLUMN>]) - FiscalYearStartMonth, 12) + 1,
        Int64.Type
    ),
