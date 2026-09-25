// fxCleanColumnNames
// Tidies column names in one step: trims spaces, turns underscores into spaces,
// collapses double spaces, and optionally applies Proper Case.
//   "  customer_first_name " -> "Customer First Name"
//
// Parameters:
//   InputTable  table to rename
//   Options     optional record:
//                 ReplaceUnderscores  default true
//                 ProperCase          default true
//                 Prefix              text to strip from the start of every name, e.g. "dbo_" (default none)
//
// Examples:
//   fxCleanColumnNames(<TABLE>)
//   fxCleanColumnNames(<TABLE>, [ProperCase = false])
//
// To promote the first row to headers first:
//   fxCleanColumnNames(Table.PromoteHeaders(<TABLE>, [PromoteAllScalars = true]))
(InputTable as table, optional Options as nullable record) as table =>
let
    opts               = if Options = null then [] else Options,
    ReplaceUnderscores = Record.FieldOrDefault(opts, "ReplaceUnderscores", true),
    ProperCase         = Record.FieldOrDefault(opts, "ProperCase", true),
    Prefix             = Record.FieldOrDefault(opts, "Prefix", null),

    CleanName = (name as text) as text =>
        let
            NoPrefix = if Prefix <> null and Text.StartsWith(name, Prefix)
                       then Text.RemoveRange(name, 0, Text.Length(Prefix))
                       else name,
            Spaced   = if ReplaceUnderscores then Text.Replace(NoPrefix, "_", " ") else NoPrefix,
            // Collapse repeated spaces and trim the ends
            Squished = Text.Combine(List.Select(Text.Split(Spaced, " "), each _ <> ""), " "),
            Cased    = if ProperCase then Text.Proper(Squished) else Squished
        in
            Cased,

    Renamed = Table.TransformColumnNames(InputTable, CleanName)
in
    Renamed
