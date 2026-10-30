// fxKeepRowsUntilMarker
// For exports with a second section or a totals block below the data you want.
// Keeps every row above the first row where MarkerColumn = MarkerValue and drops
// the marker row and everything below it.
//
// Parameters:
//   InputTable     table to trim (headers already promoted)
//   MarkerColumn   column to search, e.g. "<COLUMN>"
//   MarkerValue    value that marks where the data ends, e.g. "<VALUE>"
//   OnNotFound     optional; "original" (default) returns the whole table, "error" raises an error
//
// Example:
//   fxKeepRowsUntilMarker(<TABLE>, "<COLUMN>", "<VALUE>")
//
// Companion: fxSkipRowsUntilMarker trims the top of the same kind of export.
(InputTable as table, MarkerColumn as text, MarkerValue as any, optional OnNotFound as nullable text) as table =>
let
    Position = List.PositionOf(
        List.Transform(Table.Column(InputTable, MarkerColumn), each try Text.Trim(Text.From(_)) otherwise null),
        Text.From(MarkerValue)
    ),

    Result =
        if Position >= 0 then
            Table.FirstN(InputTable, Position)
        else if OnNotFound = "error" then
            error ("'" & Text.From(MarkerValue) & "' not found in " & MarkerColumn)
        else
            InputTable
in
    Result
