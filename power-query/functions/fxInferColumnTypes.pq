// fxInferColumnTypes
// Looks at each column's values and picks a type. Useful for files whose layout
// changes often (so a fixed "Changed Type" step keeps breaking).
//
// Rules, checked in order against the column's non-blank values:
//   1. Any value with a leading zero ("00123")    -> text  (keeps IDs, ZIP codes, account numbers intact)
//   2. Every value converts to a number
//        - all whole numbers                       -> Int64.Type
//        - otherwise                               -> number
//   3. Every value converts to a date and looks like one
//      (contains "-" or "/", or is already a date/datetime) -> date
//   4. Anything else                               -> text
//
// Every value must pass a rule (not just one value), so a column with a mix of
// numbers and text stays text. Numbers are checked before dates because
// Date.From(45000) succeeds and would turn numeric columns into dates.
//
// Parameters:
//   InputTable   table to type
//   SampleSize   optional; rows to inspect per column (default 1000). Use a larger
//                value if the first rows aren't representative.
//
// Note: this is a heuristic. Review the result, and pin important columns with
// fxSetColumnTypes afterwards when the guess matters.
(InputTable as table, optional SampleSize as nullable number) as table =>
let
    N = if SampleSize = null then 1000 else SampleSize,

    IsBlank = (v) => v = null or (v is text and Text.Trim(v) = ""),

    HasLeadingZero = (v) =>
        let t = Text.Trim(Text.From(v))
        in  Text.Length(t) > 1 and Text.StartsWith(t, "0") and not Text.StartsWith(t, "0."),

    // Only numbers and numeric text count; Number.From would also accept datetimes and logicals
    ToNumber = (v) =>
        if v is number then v
        else if v is text then (try Number.From(v, "en-US") otherwise null)
        else null,

    LooksLikeDate = (v) =>
        if v is date or v is datetime or v is datetimezone then true
        else if v is text and (Text.Contains(v, "-") or Text.Contains(v, "/"))
            then (try Date.From(v, "en-US") otherwise null) <> null
        else false,

    InferType = (values as list) as type =>
        let
            Filled = List.Select(values, each not IsBlank(_)),
            Numbers = List.Transform(Filled, ToNumber)
        in
            if List.IsEmpty(Filled) then type text
            else if List.AnyTrue(List.Transform(Filled, each _ is text and HasLeadingZero(_))) then type text
            else if List.AllTrue(List.Transform(Numbers, each _ <> null)) then
                (if List.AllTrue(List.Transform(Numbers, each Number.Round(_) = _)) then Int64.Type else type number)
            else if List.AllTrue(List.Transform(Filled, LooksLikeDate)) then type date
            else type text,

    Sample = Table.FirstN(InputTable, N),

    TypePairs = List.Transform(
        Table.ColumnNames(InputTable),
        (c) => {c, InferType(Table.Column(Sample, c))}
    ),

    ChangedTypes = Table.TransformColumnTypes(InputTable, TypePairs, "en-US")
in
    ChangedTypes
