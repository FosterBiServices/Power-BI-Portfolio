// fxSetColumnTypes
// Applies explicit column types in one step, skipping any column that doesn't
// exist in the table, and gives every column you didn't list a default type.
// Use it when source files drift (columns get added or dropped) and a hard-coded
// "Changed Type" step would break the refresh.
//
// Parameters:
//   InputTable    table to type
//   TypePairs     list of {ColumnName, Type} pairs, e.g. { {"<COLUMN_1>", type date}, {"<COLUMN_2>", Int64.Type} }
//   DefaultType   optional; the type for columns not listed in TypePairs (default: type text).
//                 Pass type any to leave unlisted columns untyped.
//
// Example:
//   fxSetColumnTypes(
//     <TABLE>,
//     {
//       {"<COLUMN_1>", type text},
//       {"<COLUMN_2>", Int64.Type},
//       {"<COLUMN_3>", type number},
//       {"<COLUMN_4>", type date}
//     }
//   )
(InputTable as table, TypePairs as list, optional DefaultType as nullable type) as table =>
let
    Default      = if DefaultType = null then type text else DefaultType,
    ExistingCols = Table.ColumnNames(InputTable),

    // Keep type rules only for columns that actually exist
    PairsForExistingCols = List.Select(TypePairs, each List.Contains(ExistingCols, _{0})),

    // Lookup record: ColumnName -> Type
    ExplicitTypeMap = Record.FromList(
        List.Transform(PairsForExistingCols, each _{1}),
        List.Transform(PairsForExistingCols, each _{0})
    ),

    // Every existing column gets its explicit type, or the default
    AllTypePairs = List.Transform(
        ExistingCols,
        (c) => {c, Record.FieldOrDefault(ExplicitTypeMap, c, Default)}
    ),

    ChangedTypes = Table.TransformColumnTypes(InputTable, AllTypePairs)
in
    ChangedTypes
