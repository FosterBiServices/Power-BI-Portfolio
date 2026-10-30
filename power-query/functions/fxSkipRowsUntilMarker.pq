// fxSkipRowsUntilMarker
// For report-style Excel/CSV exports that have title rows above the real header.
// Finds the first row where MarkerColumn = MarkerValue, removes every row above it,
// then (optionally) promotes that row to headers and trims the column names.
//
// Parameters:
//   InputTable     raw table (usually straight from Excel.Workbook / Csv.Document, columns Column1, Column2, ...)
//   MarkerColumn   column to search, e.g. "Column1"
//   MarkerValue    value that marks the header row, e.g. "<VALUE>"
//   Options        optional record:
//                    PromoteHeaders  promote the marker row to headers (default true)
//                    OnNotFound      "error" (default) raises an error; "table" returns a one-row
//                                    table with a message; "original" returns InputTable unchanged
//
// Example:
//   fxSkipRowsUntilMarker(<TABLE>, "Column1", "<VALUE>")
//
// Companion: fxKeepRowsUntilMarker trims the bottom of the same kind of export.
(InputTable as table, MarkerColumn as text, MarkerValue as any, optional Options as nullable record) as table =>
let
    opts           = if Options = null then [] else Options,
    PromoteHeaders = Record.FieldOrDefault(opts, "PromoteHeaders", true),
    OnNotFound     = Record.FieldOrDefault(opts, "OnNotFound", "error"),

    // Position of the first marker row (-1 if not found). Text.From avoids type mismatches.
    Position = List.PositionOf(
        List.Transform(Table.Column(InputTable, MarkerColumn), each try Text.Trim(Text.From(_)) otherwise null),
        Text.From(MarkerValue)
    ),

    NotFoundMessage = "'" & Text.From(MarkerValue) & "' not found in " & MarkerColumn,

    Result =
        if Position >= 0 then
            let
                // Remove all rows above the marker row
                Skipped  = Table.Skip(InputTable, Position),
                Promoted = if PromoteHeaders
                           then Table.PromoteHeaders(Skipped, [PromoteAllScalars = true])
                           else Skipped,
                // Trim spaces from column names for consistency
                Trimmed  = if PromoteHeaders
                           then Table.TransformColumnNames(Promoted, Text.Trim)
                           else Promoted
            in
                Trimmed
        else if OnNotFound = "table" then
            #table({"Error"}, {{NotFoundMessage}})
        else if OnNotFound = "original" then
            InputTable
        else
            error NotFoundMessage
in
    Result
