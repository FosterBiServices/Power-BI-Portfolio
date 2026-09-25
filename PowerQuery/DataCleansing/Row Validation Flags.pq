// Row Validation Flags
// Adds a "Reason Invalid" column that explains why a row fails a data-quality rule,
// then filters to the failures. Load the result as a separate "exceptions" table
// (or a report page) so data owners can see and fix bad rows at the source.
//
// Pattern: one validation column per rule, returning "Valid" or a reason.
// Paste into an existing query; <PREVIOUS_STEP> is the step before.


// =====================================================================
// 1) Allowed values (e.g. a score that must be 0, 1 or 2, or blank)
// =====================================================================
    AllowedValues = {"0", "1", "2"},

    ValueValidation = Table.AddColumn(
        <PREVIOUS_STEP>,
        "Reason Invalid",
        each
            let
                Value = if [<COLUMN>] = null then "" else Text.Trim(Text.From([<COLUMN>]))
            in
                if Value = "" then "Valid"                          // blanks allowed; change to "Missing Value" if not
                else if List.Contains(AllowedValues, Value) then "Valid"
                else "Invalid Value",
        type text
    ),


// =====================================================================
// 2) Date checks: missing, unparseable, in the future, too old
// =====================================================================
    EarliestValidYear = 2020,

    DateValidation = Table.AddColumn(
        <PREVIOUS_STEP>,
        "Reason Invalid",
        each
            let
                Value = [<DATE_COLUMN>]
            in
                if Value = null or Text.Trim(Text.From(Value)) = "" then
                    "Missing Date"
                else
                    let
                        Parsed = try DateTime.From(Value)
                    in
                        if Parsed[HasError] then "Invalid Date Format"
                        else if Parsed[Value] > DateTime.LocalNow() then "Future Date"
                        else if Date.Year(Parsed[Value]) < EarliestValidYear then "Date Too Old"
                        else "Valid",
        type text
    ),


// =====================================================================
// 3) Cross-column consistency: one column must match a piece of another
// ---------------------------------------------------------------------
// Example: "<COLUMN_1>" holds "CODE-LAST, FIRST" and "<COLUMN_2>" should equal "LAST".
// Text.BetweenDelimiters / BeforeDelimiter / AfterDelimiter are easier to read
// than Text.PositionOf + Text.Start + Text.Length arithmetic.
// =====================================================================
    ConsistencyValidation = Table.AddColumn(
        <PREVIOUS_STEP>,
        "Reason Invalid",
        each
            let
                Expected = Text.Upper(Text.Trim(Text.BetweenDelimiters([<COLUMN_1>], "-", ","))),
                Actual   = Text.Upper(Text.Trim(Text.From([<COLUMN_2>])))
            in
                if [<COLUMN_1>] = null or not Text.Contains([<COLUMN_1>], ",") then "Unexpected Format"
                else if Actual = Expected then "Valid"
                else "Mismatch",
        type text
    ),


// =====================================================================
// 4) Several rules at once -> first failing reason wins
// =====================================================================
    MultiRuleValidation = Table.AddColumn(
        <PREVIOUS_STEP>,
        "Reason Invalid",
        each
            if [<COLUMN_1>] = null then "Missing <COLUMN_1>"
            else if [<COLUMN_2>] < 0 then "Negative <COLUMN_2>"
            else if [<DATE_COLUMN>] > Date.From(DateTime.LocalNow()) then "Future Date"
            else "Valid",
        type text
    ),


// =====================================================================
// Keep only the failures (exceptions table)
// =====================================================================
    InvalidRows = Table.SelectRows(MultiRuleValidation, each [Reason Invalid] <> "Valid"),
