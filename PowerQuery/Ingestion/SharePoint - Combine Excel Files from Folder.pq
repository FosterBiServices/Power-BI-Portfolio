// SharePoint - Combine Excel Files from Folder
// Reads every .xlsx file in one SharePoint folder, picks a sheet from each workbook,
// promotes headers per file, and stacks them into one table.
// Unlike the built-in "Combine Files" wizard, it creates no helper queries and each
// file's headers are promoted separately, so column order can differ between files.
//
// Placeholders:
//   <SITE_URL>    https://<TENANT>.sharepoint.com/sites/<SITE>/
//   <FOLDER_URL>  full folder path as shown in [Folder Path], ending in "/"
//                 e.g. https://<TENANT>.sharepoint.com/sites/<SITE>/Shared Documents/<FOLDER>/
//   <SHEET>       sheet name, or leave SheetName = null to take the first visible sheet
//
// Follow-ups:
//   - Type the result with Functions/fxSetColumnTypes (column sets drift across files).
//   - Split timestamps with Functions/fxAddDateTimeFromPairs.
let
    // ----------------------------
    // Settings
    // ----------------------------
    SiteUrl   = "<SITE_URL>",
    FolderUrl = "<FOLDER_URL>",
    SheetName = null,                 // e.g. "<SHEET>"; null = first visible sheet
    IncludeSubfolders = false,        // true = also read files in folders below FolderUrl
    AddSourceFileColumn = true,       // adds a "Source File" column so you can trace rows back

    // ----------------------------
    // 1) List the Excel files in the folder
    // ----------------------------
    Source = SharePoint.Files(SiteUrl, [ApiVersion = 15]),

    ExcelFiles = Table.SelectRows(
        Source,
        each (if IncludeSubfolders then Text.StartsWith([Folder Path], FolderUrl) else [Folder Path] = FolderUrl)
            and Text.EndsWith(Text.Lower([Name]), ".xlsx")
            and not Text.StartsWith([Name], "~$")        // skip Office lock/temp files
    ),

    // ----------------------------
    // 2) Helper: read one workbook's sheet and promote its headers
    // ----------------------------
    GetSheetTable = (bin as binary, optional desiredSheet as nullable text) as table =>
        let
            // delayTypes = true is faster on large files
            Workbook = Excel.Workbook(bin, null, true),

            Candidates =
                if desiredSheet = null
                then Table.SelectRows(Workbook, each [Kind] = "Sheet" and ([Hidden] = null or [Hidden] = false))
                else Table.SelectRows(Workbook, each [Kind] = "Sheet" and [Name] = desiredSheet),

            // No matching sheet -> empty table instead of an error
            ChosenData =
                if Table.RowCount(Candidates) = 0
                then #table({}, {})
                else Candidates{0}[Data],

            Promoted = try Table.PromoteHeaders(ChosenData, [PromoteAllScalars = true]) otherwise ChosenData
        in
            Promoted,

    // ----------------------------
    // 3) Read each file, optionally tag it with its file name, and combine
    // ----------------------------
    PerFile = Table.AddColumn(
        ExcelFiles,
        "Data",
        each
            let
                FileName = [Name],
                Sheet    = GetSheetTable([Content], SheetName)
            in
                if AddSourceFileColumn then Table.AddColumn(Sheet, "Source File", each FileName, type text) else Sheet
    ),

    Combined =
        if Table.RowCount(PerFile) = 0
        then #table({}, {})
        else Table.Combine(PerFile[Data])
in
    Combined
