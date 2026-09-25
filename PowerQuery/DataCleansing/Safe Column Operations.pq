// Safe Column Operations
// Steps that don't fail the refresh when a column is missing, renamed, or added
// in the source. Use for Excel/CSV/SharePoint sources whose layout drifts.
// Paste the helpers and steps into an existing query; <PREVIOUS_STEP> is the step before.
//
// See also: Functions/fxSetColumnTypes (typing only the columns that exist).


// =====================================================================
// 1) Built-in "missing column" options
// ---------------------------------------------------------------------
// Most column functions accept a MissingField option as their last argument:
//   MissingField.Error (default)  fail the refresh
//   MissingField.Ignore           skip missing columns
//   MissingField.UseNull          create missing columns filled with null
// =====================================================================
    RemovedColumns = Table.RemoveColumns(<PREVIOUS_STEP>, {"<COLUMN_1>", "<COLUMN_2>"}, MissingField.Ignore),

    RenamedColumns = Table.RenameColumns(
        RemovedColumns,
        {
            {"<COLUMN_3>", "<NEW_NAME_3>"},
            {"<COLUMN_4>", "<NEW_NAME_4>"}
        },
        MissingField.Ignore
    ),

    // Guarantees a fixed output schema: missing columns are added as null
    SelectedColumns = Table.SelectColumns(RenamedColumns, {"<NEW_NAME_3>", "<NEW_NAME_4>", "<COLUMN_5>"}, MissingField.UseNull),


// =====================================================================
// 2) Transform only the columns that exist
// ---------------------------------------------------------------------
// Useful for column sets that grow over time (e.g. one column per year).
// Here: blank text -> null, everything else -> number.
// =====================================================================
    ColumnsToFix = {"<COLUMN_1>", "<COLUMN_2>", "<COLUMN_3>"},

    // Or build the list by pattern instead of by name:
    //   ColumnsToFix = List.Select(Table.ColumnNames(<PREVIOUS_STEP>), each Text.StartsWith(_, "<PREFIX>")),

    ExistingColumnsToFix = List.Intersect({ColumnsToFix, Table.ColumnNames(<PREVIOUS_STEP>)}),

    TransformedColumns = Table.TransformColumns(
        <PREVIOUS_STEP>,
        List.Transform(
            ExistingColumnsToFix,
            each {_, (val) => if val = null or Text.Trim(Text.From(val)) = "" then null else Number.From(val), type number}
        )
    ),


// =====================================================================
// 3) Reusable safe helpers
// ---------------------------------------------------------------------
// Define these once at the top of the query, then call them like functions.
// =====================================================================
    SafeDuplicate =
        (tbl as table, col as text, newCol as text) as table =>
            if Table.HasColumns(tbl, col) then Table.DuplicateColumn(tbl, col, newCol) else tbl,

    SafeRemove =
        (tbl as table, cols as list) as table =>
            Table.RemoveColumns(tbl, cols, MissingField.Ignore),

    // Replaces whole values using a record of Old = New pairs (see "Replace Values from Mapping.pq")
    SafeMapReplace =
        (tbl as table, col as text, map as record) as table =>
            if Table.HasColumns(tbl, col)
            then Table.TransformColumns(tbl, {{col, each Record.FieldOrDefault(map, _, _), type text}})
            else tbl,

    // Merges whichever of the listed columns exist into one text column
    SafeMerge =
        (tbl as table, cols as list, newCol as text, optional delimiter as nullable text) as table =>
            let
                Existing = List.Intersect({cols, Table.ColumnNames(tbl)})
            in
                if List.Count(Existing) > 0
                then Table.CombineColumns(
                        Table.TransformColumnTypes(tbl, List.Transform(Existing, each {_, type text})),
                        Existing,
                        Combiner.CombineTextByDelimiter(if delimiter = null then " " else delimiter, QuoteStyle.None),
                        newCol
                     )
                else tbl,

    // Example usage
    AfterDuplicate = SafeDuplicate(<PREVIOUS_STEP>, "<COLUMN_1>", "<COLUMN_1> - Copy"),
    AfterMerge     = SafeMerge(AfterDuplicate, {"<COLUMN_1> - Copy", "<COLUMN_2>"}, "<NEW_COLUMN_NAME>", " "),
    AfterRemove    = SafeRemove(AfterMerge, {"<COLUMN_3>", "<COLUMN_4>"}),
