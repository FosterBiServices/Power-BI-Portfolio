// Replace Values from Mapping
// Replace many values at once (codes -> names, old labels -> new labels) instead of
// stacking one "Replaced Value" step per value.
// Paste into an existing query; <PREVIOUS_STEP> is the step before.


// =====================================================================
// 1) Mapping kept in a lookup table (best when business users maintain it)
// ---------------------------------------------------------------------
// <LOOKUP_TABLE> has two columns: the old value and the new value,
// e.g. state abbreviations -> state names. Whole-cell matches only.
// =====================================================================
    // List of {Old, New} pairs from the lookup table
    ReplacementPairs = List.Buffer(
        Table.ToRows(
            Table.TransformColumnTypes(
                Table.SelectColumns(<LOOKUP_TABLE>, {"<OLD_VALUE_COLUMN>", "<NEW_VALUE_COLUMN>"}),
                {{"<OLD_VALUE_COLUMN>", type text}, {"<NEW_VALUE_COLUMN>", type text}}
            )
        )
    ),

    // Apply to specific columns...
    ReplacedInColumns = Table.TransformColumns(
        <PREVIOUS_STEP>,
        {
            {"<COLUMN_1>", each List.ReplaceMatchingItems({_}, ReplacementPairs){0}, type text},
            {"<COLUMN_2>", each List.ReplaceMatchingItems({_}, ReplacementPairs){0}, type text}
        }
    ),

    // ...or to every column (empty operations list + default transformation)
    ReplacedEverywhere = Table.TransformColumns(
        <PREVIOUS_STEP>,
        {},
        each List.ReplaceMatchingItems({_}, ReplacementPairs){0}
    ),


// =====================================================================
// 2) Mapping written inline as a record (best for a short, stable list)
// ---------------------------------------------------------------------
// Use #"..." for keys with spaces or punctuation. Values not in the map pass through.
// =====================================================================
    ValueMap = [
        #"<OLD_VALUE_1>" = "<NEW_VALUE_1>",
        #"<OLD_VALUE_2>" = "<NEW_VALUE_2>"
    ],

    MappedColumn = Table.TransformColumns(
        <PREVIOUS_STEP>,
        {{"<COLUMN>", each Record.FieldOrDefault(ValueMap, Text.From(_), _), type text}}
    ),


// =====================================================================
// 3) Partial (substring) replacements across several columns
// ---------------------------------------------------------------------
// Table.ReplaceValue with Replacer.ReplaceText changes text inside the cell;
// List.Accumulate applies each pair in turn.
// =====================================================================
    TextPairs = {
        {"<OLD_TEXT_1>", "<NEW_TEXT_1>"},
        {"<OLD_TEXT_2>", "<NEW_TEXT_2>"}
    },

    ReplacedText = List.Accumulate(
        TextPairs,
        <PREVIOUS_STEP>,
        (state, pair) => Table.ReplaceValue(state, pair{0}, pair{1}, Replacer.ReplaceText, {"<COLUMN_1>", "<COLUMN_2>"})
    ),


// =====================================================================
// 4) Nulls -> 0 in numeric columns (before summing or dividing)
// =====================================================================
    NullsToZero = Table.ReplaceValue(<PREVIOUS_STEP>, null, 0, Replacer.ReplaceValue, {"<COLUMN_1>", "<COLUMN_2>"}),
