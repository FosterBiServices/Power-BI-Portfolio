// Excel - Connect and Select Sheet
// Three ways to point at a single Excel workbook and pick the sheet you need.
// Each block is a separate query; copy the one you need.


// =====================================================================
// 1) Build the file URL from parameters
// ---------------------------------------------------------------------
// Create these as Parameters (Manage Parameters > New), not as queries.
// Splitting the path lets you repoint many queries at another site or
// user folder by editing one parameter.
//
//   SiteURL   "https://<TENANT>.sharepoint.com/sites/<SITE>/Shared%20Documents/<FOLDER>/"
//             meta [IsParameterQuery = true, Type = "Text", IsParameterQueryRequired = true]
//   SubFolder "<SUBFOLDER>/"
//             meta [IsParameterQuery = true, Type = "Text", IsParameterQueryRequired = true]
//   FileName  "<FILE>.xlsx"
//             meta [IsParameterQuery = true, Type = "Text", IsParameterQueryRequired = true]
// =====================================================================
let
    Source = Excel.Workbook(Web.Contents(SiteURL & SubFolder & FileName), true, true),
    // Pick the sheet by name (Kind = "Table" for a formatted Excel table, "DefinedName" for a named range)
    SheetData = Source{[Item = "<SHEET>", Kind = "Sheet"]}[Data]
in
    SheetData


// =====================================================================
// 2) Pick the Nth sheet instead of a sheet name
// ---------------------------------------------------------------------
// Use when the sheet name changes every month (e.g. "Jan 2025", "Feb 2025")
// but its position in the workbook doesn't.
// =====================================================================
let
    n = 1,    // 1 = first sheet, 5 = fifth sheet

    Source = Excel.Workbook(Web.Contents("<FILE_URL>"), null, true),

    SheetsOnly  = Table.Buffer(Table.SelectRows(Source, each [Kind] = "Sheet")),
    CountSheets = Table.RowCount(SheetsOnly),

    // Guard against an out-of-range n with a readable message
    NthSheetRow =
        if n >= 1 and n <= CountSheets
        then SheetsOnly{n - 1}
        else error Text.Format("Requested sheet index (#[n]) is out of range (1..#[m]).", [n = n, m = CountSheets]),

    NthSheetData = NthSheetRow[Data],
    Promoted     = Table.PromoteHeaders(NthSheetData, [PromoteAllScalars = true])

    // Typical follow-ups:
    //   Trimmed = fxSkipRowsUntilMarker(NthSheetData, "Column1", "<VALUE>"),
    //   Cleaned = fxCleanColumnNames(Trimmed),
    //   Removed = Table.RemoveColumns(Cleaned, {"<COLUMN_1>", "<COLUMN_2>"}, MissingField.Ignore),
    //   Typed   = fxSetColumnTypes(Removed, { {"<COLUMN_3>", type date}, {"<COLUMN_4>", type text} })
in
    Promoted


// =====================================================================
// 3) Pick a sheet by name pattern
// ---------------------------------------------------------------------
// Takes the first sheet whose name contains a keyword (case-insensitive).
// =====================================================================
let
    Keyword = "<SHEET_KEYWORD>",

    Source   = Excel.Workbook(Web.Contents("<FILE_URL>"), null, true),
    Matches  = Table.SelectRows(Source, each [Kind] = "Sheet" and Text.Contains([Name], Keyword, Comparer.OrdinalIgnoreCase)),
    Data     = if Table.IsEmpty(Matches) then error ("No sheet name contains '" & Keyword & "'") else Matches{0}[Data],
    Promoted = Table.PromoteHeaders(Data, [PromoteAllScalars = true])
in
    Promoted
