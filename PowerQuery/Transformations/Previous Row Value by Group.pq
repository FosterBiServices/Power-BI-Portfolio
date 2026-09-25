// Previous Row Value by Group
// Adds the previous (or next) row's value within each group, e.g. the prior score
// for the same location, the previous reading for the same meter, or the prior
// status of the same ticket. Equivalent to SQL LAG()/LEAD() OVER (PARTITION BY ... ORDER BY ...).
//
// Why Table.Combine at the end: combining the nested tables keeps every column's
// data type, so you don't need to expand each column and re-type it.
let
    Source = <TABLE>,

    // 1) Sort within each group. Table.Buffer locks in the sort order before grouping.
    Sorted = Table.Buffer(
        Table.Sort(
            Source,
            {
                {"<GROUP_COLUMN>", Order.Ascending},
                {"<DATE_COLUMN>",  Order.Descending}    // newest first
            }
        )
    ),

    // 2) One nested table per group ("each _" keeps all rows and columns)
    Grouped = Table.Group(Sorted, {"<GROUP_COLUMN>"}, {{"Rows", each _, type table}}),

    // 3) Inside each group: add an index, then look up the neighbouring row's value.
    //    With newest-first sorting, Index + 1 is the previous (older) row.
    //    Use Index - 1 for the next (newer) row.
    WithPrevious = Table.TransformColumns(
        Grouped,
        {{
            "Rows",
            (GroupRows as table) =>
                let
                    Indexed = Table.AddIndexColumn(GroupRows, "Index", 0, 1, Int64.Type),
                    Values  = List.Buffer(Indexed[<VALUE_COLUMN>]),
                    AddPrev = Table.AddColumn(
                        Indexed,
                        "Previous <VALUE_COLUMN>",
                        each try Values{[Index] + 1} otherwise null,
                        type number
                    )
                in
                    Table.RemoveColumns(AddPrev, {"Index"}),
            type table
        }}
    ),

    // 4) Stack the groups back together with types intact
    Output = Table.Combine(WithPrevious[Rows]),

    // Optional: change vs. previous
    AddChange = Table.AddColumn(
        Output,
        "Change",
        each if [#"Previous <VALUE_COLUMN>"] = null then null else [<VALUE_COLUMN>] - [#"Previous <VALUE_COLUMN>"],
        type number
    )
in
    AddChange
