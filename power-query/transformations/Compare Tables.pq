// Compare Tables
// Find rows that exist in one table but not the other, e.g. to reconcile two
// extracts, check a migration, or see what changed between two snapshots.


// =====================================================================
// 1) Whole-row comparison: rows in <TABLE_2> that are not in <TABLE>
// ---------------------------------------------------------------------
// Every column must match. Both tables need the same column names.
// =====================================================================
let
    NewOrChangedRows = Table.RemoveMatchingRows(<TABLE_2>, Table.ToRecords(<TABLE>))
in
    NewOrChangedRows


// =====================================================================
// 2) Key-based comparison with an anti join (faster on large tables)
// =====================================================================
let
    // Keys in <TABLE_2> missing from <TABLE> (added rows)
    Added = Table.NestedJoin(<TABLE_2>, {"<KEY_COLUMN>"}, <TABLE>, {"<KEY_COLUMN>"}, "Match", JoinKind.LeftAnti),

    // Keys in <TABLE> missing from <TABLE_2> (removed rows)
    Removed = Table.NestedJoin(<TABLE>, {"<KEY_COLUMN>"}, <TABLE_2>, {"<KEY_COLUMN>"}, "Match", JoinKind.LeftAnti),

    // One table with a status column
    Result = Table.Combine({
        Table.AddColumn(Table.RemoveColumns(Added, {"Match"}),   "Status", each "Added",   type text),
        Table.AddColumn(Table.RemoveColumns(Removed, {"Match"}), "Status", each "Removed", type text)
    })
in
    Result


// =====================================================================
// 3) Same key, different value (changed rows)
// =====================================================================
let
    Joined   = Table.NestedJoin(<TABLE>, {"<KEY_COLUMN>"}, <TABLE_2>, {"<KEY_COLUMN>"}, "New", JoinKind.Inner),
    Expanded = Table.ExpandTableColumn(Joined, "New", {"<COLUMN>"}, {"New <COLUMN>"}),
    Changed  = Table.SelectRows(Expanded, each [<COLUMN>] <> [#"New <COLUMN>"])
in
    Changed
