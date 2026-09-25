// fxReplaceErrorsInAllColumns
// Replaces error values in every column (or a chosen list of columns) with a single value.
// Handy after a type change on messy source data, so one bad cell doesn't fail the refresh.
//
// Parameters:
//   InputTable   table to clean
//   Replacement  optional; value to use instead of the error (default null)
//   Columns      optional; list of columns to clean (default: all columns)
//
// Examples:
//   fxReplaceErrorsInAllColumns(<TABLE>)
//   fxReplaceErrorsInAllColumns(<TABLE>, 0, {"<COLUMN_1>", "<COLUMN_2>"})
//
// Inline equivalent (no function needed):
//   Table.ReplaceErrorValues(<TABLE>, List.Transform(Table.ColumnNames(<TABLE>), each {_, null}))
(InputTable as table, optional Replacement as any, optional Columns as nullable list) as table =>
let
    TargetCols = if Columns = null
                 then Table.ColumnNames(InputTable)
                 else List.Intersect({Columns, Table.ColumnNames(InputTable)}),

    Replaced = Table.ReplaceErrorValues(
        InputTable,
        List.Transform(TargetCols, each {_, Replacement})
    )
in
    Replaced
