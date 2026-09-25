// Merge Between Dates (range lookup)
// Joins each row to the lookup row whose date range contains the row's date,
// e.g. the price, rate, plan, or assignment that was in effect on a transaction date.
// A normal merge only matches on equal keys; this matches key AND date-in-range.
//
// <TABLE>          fact rows with a key and an event date
// <LOOKUP_TABLE>   rows with the same key plus <START_DATE_COLUMN> / <END_DATE_COLUMN>
//                  (end date exclusive; null end = still active)
let
    Source = <TABLE>,

    // Buffer the lookup once so it isn't re-read for every fact row
    BufferedLookup = Table.Buffer(
        Table.SelectColumns(
            <LOOKUP_TABLE>,
            {"<KEY_COLUMN>", "<START_DATE_COLUMN>", "<END_DATE_COLUMN>", "<COLUMN_1>", "<COLUMN_2>"}
        )
    ),

    // For each fact row (S), keep lookup rows (L) with the same key whose range contains the date
    Matched = Table.AddColumn(
        Source,
        "Lookup",
        (S) =>
            Table.SelectRows(
                BufferedLookup,
                (L) =>
                    L[<KEY_COLUMN>] = S[<KEY_COLUMN>]
                    and S[<DATE_COLUMN>] >= L[<START_DATE_COLUMN>]
                    and (L[<END_DATE_COLUMN>] = null or S[<DATE_COLUMN>] < L[<END_DATE_COLUMN>])
            ),
        type table
    ),

    // Expanding a table column duplicates rows when more than one range matches;
    // keep the first match if ranges can overlap:
    //   FirstMatch = Table.TransformColumns(Matched, {{"Lookup", each Table.FirstN(_, 1), type table}}),

    Expanded = Table.ExpandTableColumn(Matched, "Lookup", {"<COLUMN_1>", "<COLUMN_2>"}, {"<COLUMN_1>", "<COLUMN_2>"})
in
    Expanded

// Performance: this is a row-by-row scan (fact rows x lookup rows). For large tables,
// merge on the key first (Table.NestedJoin), then filter each nested table by date:
//   Joined   = Table.NestedJoin(Source, {"<KEY_COLUMN>"}, BufferedLookup, {"<KEY_COLUMN>"}, "Lookup", JoinKind.LeftOuter),
//   InRange  = Table.AddColumn(Joined, "InRange", (S) => Table.SelectRows(S[Lookup], (L) =>
//                  S[<DATE_COLUMN>] >= L[<START_DATE_COLUMN>] and (L[<END_DATE_COLUMN>] = null or S[<DATE_COLUMN>] < L[<END_DATE_COLUMN>]))),
//   Cleaned  = Table.RemoveColumns(InRange, {"Lookup"}),
//   Expanded = Table.ExpandTableColumn(Cleaned, "InRange", {"<COLUMN_1>", "<COLUMN_2>"})
