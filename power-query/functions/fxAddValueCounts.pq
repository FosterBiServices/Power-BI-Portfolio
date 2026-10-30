// fxAddValueCounts
// Counts, row by row, how many of a set of columns hold each value, and adds one
// count column per value. Built for survey/audit/checklist data where each question
// is a column scored 0/1/2 (or Yes/No/NA) and you need per-row totals.
//
// Parameters:
//   SourceTable   table to extend
//   ValueLabels   list of {Value, OutputColumnName}, e.g. { {0, "Count of 0"}, {1, "Count of 1"} }
//   Columns       optional; the columns to count across. Default: every "numbered question"
//                 column, i.e. names like "1. <COLUMN>", "12. <COLUMN>" (digits before the first ".").
//   ExcludeColumns optional; columns to leave out of the default selection
//
// Examples:
//   fxAddValueCounts(
//     <TABLE>,
//     { {0, "Count of 0"}, {1, "Count of 1"}, {2, "Count of 2"} }
//   )
//
//   fxAddValueCounts(
//     <TABLE>,
//     { {"Yes", "Yes Count"}, {"No", "No Count"} },
//     {"<COLUMN_1>", "<COLUMN_2>", "<COLUMN_3>"}
//   )
//
// Tip: add a combined column afterwards, e.g. Eligible = [Count of 0] + [Count of 1].
(
    SourceTable as table,
    ValueLabels as list,
    optional Columns as nullable list,
    optional ExcludeColumns as nullable list
) as table =>
let
    Excluded = if ExcludeColumns = null then {} else ExcludeColumns,

    // Default column selection: "<number>. <text>" style names
    NumberedColumns = List.Select(
        Table.ColumnNames(SourceTable),
        each Text.Contains(_, ".")
            and (try Number.From(Text.BeforeDelimiter(_, ".")) otherwise null) <> null
            and not List.Contains(Excluded, _)
    ),

    CountColumns = if Columns = null then NumberedColumns else Columns,
    OutputNames  = List.Transform(ValueLabels, each _{1}),

    // One record per row holding every count, then expand it
    AddCounts = Table.AddColumn(
        SourceTable,
        "__Counts",
        (row) =>
            let
                Values = Record.ToList(Record.SelectFields(row, CountColumns, MissingField.Ignore))
            in
                Record.FromList(
                    List.Transform(ValueLabels, (vl) => List.Count(List.Select(Values, each _ = vl{0}))),
                    OutputNames
                ),
        type record
    ),

    Expanded = Table.ExpandRecordColumn(AddCounts, "__Counts", OutputNames),

    Typed = Table.TransformColumnTypes(Expanded, List.Transform(OutputNames, each {_, Int64.Type}))
in
    Typed
