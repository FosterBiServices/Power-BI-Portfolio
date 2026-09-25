// fxConvertColumnsUtcToEastern
// Converts one or more UTC columns in a table to US Eastern, applying DST.
// Requires fxUtcToEastern in the same model.
//
// Parameters:
//   tbl       table to transform
//   columns   list of column names to convert
//   KeepZone  optional; true -> datetimezone, false/null -> datetime
//   IgnoreMissing optional; true skips columns that don't exist (default false = error)
//
// Example:
//   fxConvertColumnsUtcToEastern(<TABLE>, {"<COLUMN_1>", "<COLUMN_2>"})
(tbl as table, columns as list, optional KeepZone as nullable logical, optional IgnoreMissing as nullable logical) as table =>
let
    Keep = if KeepZone = null then false else KeepZone,

    // One transform operation per requested column
    Operations =
        List.Transform(
            columns,
            (c) => {c, each fxUtcToEastern(_, Keep), if Keep then type datetimezone else type datetime}
        ),

    Converted = Table.TransformColumns(
        tbl,
        Operations,
        null,
        if IgnoreMissing = true then MissingField.Ignore else MissingField.Error
    )
in
    Converted
