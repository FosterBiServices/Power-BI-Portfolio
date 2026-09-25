// Name Formatting
// Build "Last, First" display names from separate columns, for one person or for a
// whole hierarchy (employee, manager, director, ...), and parse names out of an
// email address / user principal name.
// Paste into an existing query; <PREVIOUS_STEP> is the step before.


// =====================================================================
// 1) One name column
// ---------------------------------------------------------------------
// Text.Combine skips nulls, so a missing first name gives "Smith" rather than
// "Smith, " or an error.
// =====================================================================
    AddFullName = Table.AddColumn(
        <PREVIOUS_STEP>,
        "Full Name",
        each Text.Combine(List.RemoveNulls({[<LAST_NAME_COLUMN>], [<FIRST_NAME_COLUMN>]}), ", "),
        type text
    ),


// =====================================================================
// 2) Many name columns at once (e.g. every level of a reporting hierarchy)
// ---------------------------------------------------------------------
// One {NewColumn, LastNameColumn, FirstNameColumn} entry per level,
// instead of one "Added Custom" step per level.
// =====================================================================
    NameColumns = {
        {"<NEW_COLUMN_1>", "<LAST_NAME_COLUMN_1>", "<FIRST_NAME_COLUMN_1>"},
        {"<NEW_COLUMN_2>", "<LAST_NAME_COLUMN_2>", "<FIRST_NAME_COLUMN_2>"},
        {"<NEW_COLUMN_3>", "<LAST_NAME_COLUMN_3>", "<FIRST_NAME_COLUMN_3>"}
    },

    AddAllNames = List.Accumulate(
        NameColumns,
        <PREVIOUS_STEP>,
        (state, cols) =>
            Table.AddColumn(
                state,
                cols{0},
                (row) => Text.Combine(
                    List.RemoveNulls({Record.Field(row, cols{1}), Record.Field(row, cols{2})}),
                    ", "
                ),
                type text
            )
    ),


// =====================================================================
// 3) "first.last@domain.com" -> "Last, First"
// =====================================================================
    AddNameFromEmail = Table.AddColumn(
        <PREVIOUS_STEP>,
        "Name From Email",
        each
            let
                LocalPart = Text.BeforeDelimiter([<EMAIL_COLUMN>], "@"),
                First     = Text.Proper(Text.BeforeDelimiter(LocalPart, ".")),
                Last      = Text.Proper(Text.AfterDelimiter(LocalPart, "."))
            in
                if [<EMAIL_COLUMN>] = null or not Text.Contains(LocalPart, ".") then null
                else Last & ", " & First,
        type text
    ),


// =====================================================================
// DAX equivalent for the signed-in user (e.g. a "Welcome, Last, First" card)
// ---------------------------------------------------------------------
// USERPRINCIPALNAME() is evaluated at query time, so this has to be a measure;
// Power Query can't see who is viewing the report.
// =====================================================================
// Current User Name =
// VAR UPN      = USERPRINCIPALNAME ()
// VAR DotPos   = SEARCH ( ".", UPN, 1, 0 )
// VAR AtPos    = SEARCH ( "@", UPN, 1, 0 )
// RETURN
//     IF (
//         DotPos > 0 && AtPos > DotPos,
//         MID ( UPN, DotPos + 1, AtPos - DotPos - 1 ) & ", " & LEFT ( UPN, DotPos - 1 ),
//         UPN
//     )
