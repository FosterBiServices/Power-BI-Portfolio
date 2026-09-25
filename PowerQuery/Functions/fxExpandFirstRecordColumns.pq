// fxExpandFirstRecordColumns
// Expands several list-of-record columns at once, taking the first record in each list.
// Typical use: SharePoint list "Person or Group" columns, which arrive as a list of
// records (title, email, ...) even when only one person is selected.
//
// Parameters:
//   SourceTable  table to expand
//   Columns      list of column names to expand
//   Fields       optional; record fields to pull out (default {"title", "email"})
//   Suffixes     optional; suffix for each new column, same order as Fields (default {" Name", " Email"})
//
// Example:
//   fxExpandFirstRecordColumns(<TABLE>, {"<COLUMN_1>", "<COLUMN_2>"})
//   -> "<COLUMN_1> Name", "<COLUMN_1> Email", "<COLUMN_2> Name", "<COLUMN_2> Email"
(SourceTable as table, Columns as list, optional Fields as nullable list, optional Suffixes as nullable list) as table =>
let
    FieldList  = if Fields = null then {"title", "email"} else Fields,
    SuffixList = if Suffixes = null then {" Name", " Email"} else Suffixes,

    // Replace each list with its first record (null if the list is empty or not a list)
    FirstItems = Table.TransformColumns(
        SourceTable,
        List.Transform(Columns, each {_, each try _{0} otherwise null})
    ),

    Expanded = List.Accumulate(
        Columns,
        FirstItems,
        (state, col) =>
            Table.ExpandRecordColumn(
                state,
                col,
                FieldList,
                List.Transform(SuffixList, each col & _)
            )
    )
in
    Expanded
