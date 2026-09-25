// fxAddDateTimeFromPairs
// For each source column, adds "<prefix> date", "<prefix> time" and "<prefix> datekey"
// (yyyyMMdd integer) columns. Handles text, date, datetime, datetimezone and time inputs.
// Useful for splitting timestamps into a date (to relate to a date table) and a time.
//
// Parameters:
//   InputTable   table to extend
//   Pairs        list of {SourceColumn, OutputPrefix}
//   Options      optional record:
//                  KeepOriginalColumns  keep the source columns (default true)
//                  Overwrite            replace output columns that already exist (default true)
//                  Culture              culture for parsing text, e.g. "en-US", "en-GB" (default null = current)
//
// Example:
//   fxAddDateTimeFromPairs(
//     <TABLE>,
//     {
//       {"<COLUMN_1>", "Opened"},
//       {"<COLUMN_2>", "Resolved"}
//     },
//     [KeepOriginalColumns = true, Overwrite = true, Culture = "en-US"]
//   )
//   -> adds "Opened date", "Opened time", "Opened datekey", "Resolved date", ...
let
  fxAddDateTimeFromPairs =
    (
      InputTable as table,
      Pairs      as list,
      optional Options as nullable record
    )
    as table =>
    let
      // ----- Options -----
      opts         = if Options = null then [] else Options,
      KeepOriginal = Record.FieldOrDefault(opts, "KeepOriginalColumns", true),
      Overwrite    = Record.FieldOrDefault(opts, "Overwrite", true),
      Culture      = Record.FieldOrDefault(opts, "Culture", null),

      // ----- Helpers -----
      FeatureNames = (p as text) as list =>
        {
          p & " date",
          p & " time",
          p & " datekey"
        },

      // Coerce any value to datetime; text is parsed with DateTime.FromText
      ToDateTime = (v as any, optional culture as nullable text) as nullable datetime =>
        if v = null then
          null
        else if Value.Is(v, type datetime) then
          v
        else if Value.Is(v, type datetimezone) then
          DateTimeZone.RemoveZone(v)
        else if Value.Is(v, type date) then
          DateTime.From(v)
        else if Value.Is(v, type time) then
          // Anchor time-only values to the Excel epoch day
          #datetime(1899, 12, 30, Time.Hour(v), Time.Minute(v), Time.Second(v))
        else if Value.Is(v, type text) then
          try (if culture = null then DateTime.FromText(v) else DateTime.FromText(v, culture)) otherwise null
        else
          try (if culture = null then DateTime.From(v) else DateTime.From(v, culture)) otherwise null,

      EnsureWritable = (tbl as table, outName as text) as table =>
        if Overwrite and Table.HasColumns(tbl, outName)
        then Table.RemoveColumns(tbl, outName)
        else tbl,

      // ----- Validate inputs -----
      SourceCols = List.Transform(Pairs, each _{0}),
      Missing    = List.Difference(SourceCols, Table.ColumnNames(InputTable)),
      Checked    = if List.Count(Missing) > 0
                   then error ("These columns were not found: " & Text.Combine(Missing, ", "))
                   else InputTable,

      // ----- Add derived columns for each pair -----
      WithDerived =
        List.Accumulate(
          Pairs,
          Checked,
          (state as table, current as list) =>
            let
              colName  = current{0},
              outNames = FeatureNames(current{1}),

              WithDate =
                Table.AddColumn(
                  EnsureWritable(state, outNames{0}),
                  outNames{0},
                  (r as record) =>
                    let dt = ToDateTime(Record.Field(r, colName), Culture)
                    in  if dt = null then null else Date.From(dt),
                  type date
                ),

              WithTime =
                Table.AddColumn(
                  EnsureWritable(WithDate, outNames{1}),
                  outNames{1},
                  (r as record) =>
                    let dt = ToDateTime(Record.Field(r, colName), Culture)
                    in  if dt = null then null else Time.From(dt),
                  type time
                ),

              WithDateKey =
                Table.AddColumn(
                  EnsureWritable(WithTime, outNames{2}),
                  outNames{2},
                  (r as record) =>
                    let dt = ToDateTime(Record.Field(r, colName), Culture)
                    in  if dt = null then null
                        else Number.FromText(Date.ToText(Date.From(dt), "yyyyMMdd")),
                  Int64.Type
                )
            in
              WithDateKey
        ),

      // Drop the source columns last so the derivations can still read them
      Result =
        if KeepOriginal
        then WithDerived
        else Table.RemoveColumns(WithDerived, SourceCols)
    in
      Result
in
  fxAddDateTimeFromPairs
