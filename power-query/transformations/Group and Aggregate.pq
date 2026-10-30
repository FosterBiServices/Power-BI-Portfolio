// Group and Aggregate
// Pre-aggregating in Power Query for a summary table: filter to the latest period,
// group, add ratio columns, and roll up a second time.
// Prefer DAX measures over stored ratios when users need to slice freely; use this
// for fixed summary/scorecard tables or to shrink a very large fact table.
let
    Source = <TABLE>,

    // -----------------------------------------------------------------
    // 1) Keep only the most recent year in the data (moves forward automatically)
    // -----------------------------------------------------------------
    LatestYear     = List.Max(Source[<YEAR_COLUMN>]),
    LatestYearOnly = Table.SelectRows(Source, each [<YEAR_COLUMN>] = LatestYear),

    // Or only complete weeks (drop the current, partial week):
    //   CompleteWeeks = Table.SelectRows(Source, each [<DATE_COLUMN>] < Date.StartOfWeek(Date.From(DateTime.LocalNow()), Day.Sunday)),

    // -----------------------------------------------------------------
    // 2) Group to one row per day + category, summing the measures
    // -----------------------------------------------------------------
    // Grouping drops every column not listed, so there's no need to remove them first.
    GroupedByDay = Table.Group(
        LatestYearOnly,
        {"<DATE_COLUMN>", "<PERIOD_COLUMN>", "<CATEGORY_COLUMN>"},
        {
            {"<MEASURE_1>", each List.Sum([<COLUMN_1>]), type number},
            {"<MEASURE_2>", each List.Sum([<COLUMN_2>]), type number},
            {"Numerator",   each List.Sum([<COLUMN_3>]), type number},
            {"Denominator", each List.Sum([<COLUMN_4>]), type number},
            {"Max Value",   each List.Max([<COLUMN_5>]), type number},
            {"Row Count",   each Table.RowCount(_), Int64.Type}
        }
    ),

    // List.Sum of only nulls returns null; turn those into 0 before dividing
    NullsToZero = Table.ReplaceValue(GroupedByDay, null, 0, Replacer.ReplaceValue, {"<MEASURE_1>", "<MEASURE_2>"}),

    // 1 on days with activity, used as a "days worked" denominator after the roll-up
    AddActiveDay = Table.AddColumn(NullsToZero, "Active Day", each if [<MEASURE_1>] > 0 then 1 else 0, Int64.Type),

    // -----------------------------------------------------------------
    // 3) Roll up again from day level to period level
    // -----------------------------------------------------------------
    GroupedByPeriod = Table.Group(
        AddActiveDay,
        {"<PERIOD_COLUMN>", "<CATEGORY_COLUMN>"},
        {
            {"<MEASURE_1>",  each List.Sum([<MEASURE_1>]), type number},
            {"<MEASURE_2>",  each List.Sum([<MEASURE_2>]), type number},
            {"Numerator",    each List.Sum([Numerator]), type number},
            {"Denominator",  each List.Sum([Denominator]), type number},
            {"Active Days",  each List.Sum([Active Day]), Int64.Type}
        }
    ),

    // -----------------------------------------------------------------
    // 4) Ratio columns (guard every division against zero)
    // -----------------------------------------------------------------
    SafeDivide = (n as nullable number, d as nullable number) as nullable number =>
        if d = null or d = 0 or n = null then null else n / d,

    AddRate = Table.AddColumn(GroupedByPeriod, "Rate", each SafeDivide([Numerator], [Denominator]), Percentage.Type),

    // e.g. units per hour when <MEASURE_1> is stored in seconds
    AddPerHour = Table.AddColumn(AddRate, "<MEASURE_2> per Hour", each SafeDivide([<MEASURE_2>], [<MEASURE_1>] / 3600), type number),

    // e.g. average daily FTE from hours worked (7.5-hour day)
    AddFTE = Table.AddColumn(AddPerHour, "FTE", each SafeDivide([<MEASURE_1>] / 3600 / 7.5, [Active Days]), type number),

    // -----------------------------------------------------------------
    // 5) Drop helper columns and rename for the report
    // -----------------------------------------------------------------
    RemovedHelpers = Table.RemoveColumns(AddFTE, {"Numerator", "Denominator", "Active Days"}),
    Renamed        = Table.RenameColumns(RemovedHelpers, {{"<PERIOD_COLUMN>", "Period"}})
in
    Renamed
