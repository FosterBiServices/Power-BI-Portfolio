// Database and Dataflow Sources
// Connection patterns that keep server/database/workspace details in parameters,
// so the same query can move between Dev/Test/Prod without editing M.
// Each block is a separate query; copy the one you need.
//
// Parameters (Manage Parameters > New, Type = Text):
//   Server       "<SERVER>"
//   Database     "<DATABASE>"
//   WorkspaceId  "<WORKSPACE_ID>"   (GUID)
//   DataflowId   "<DATAFLOW_ID>"    (GUID)


// =====================================================================
// 1) SQL Server table or view, selecting columns early
// ---------------------------------------------------------------------
// Selecting columns right after navigation folds into the SQL SELECT,
// so unused columns are never pulled across the network.
// =====================================================================
let
    Source = Sql.Database(Server, Database),
    Data   = Source{[Schema = "<SCHEMA>", Item = "<TABLE>"]}[Data],

    // Keep only what the model needs (folds to SQL)
    KeptColumns = Table.SelectColumns(Data, {"<COLUMN_1>", "<COLUMN_2>", "<COLUMN_3>"}),

    // Drop audit/technical columns if you'd rather list what to remove
    //   Removed = Table.RemoveColumns(Data, {"<COLUMN_4>", "<COLUMN_5>"}, MissingField.Ignore),

    // Row filters on source columns also fold into the WHERE clause
    FilteredRows = Table.SelectRows(KeptColumns, each [<COLUMN_1>] >= #date(2020, 1, 1))
in
    FilteredRows


// =====================================================================
// 2) Pick the database at run time from the server's database list
// ---------------------------------------------------------------------
// Sql.Databases lists every database; handy when the database name itself
// is a parameter that changes between environments.
// =====================================================================
let
    Source = Sql.Databases(Server),
    Db     = Source{[Name = Database]}[Data],
    Data   = Db{[Schema = "<SCHEMA>", Item = "<TABLE>"]}[Data]
in
    Data


// =====================================================================
// 3) Join two tables from the same database, then expand
// ---------------------------------------------------------------------
// The [[col],[col]] projection keeps only the listed columns. Both sides come
// from the same source, so the join folds into a single SQL statement.
// =====================================================================
let
    Source = Sql.Database(Server, Database),

    LeftTable  = Source{[Schema = "<SCHEMA>", Item = "<TABLE>"]}[Data][[<KEY_COLUMN>], [<COLUMN_1>], [<COLUMN_2>]],
    RightTable = Source{[Schema = "<SCHEMA>", Item = "<TABLE_2>"]}[Data][[<KEY_COLUMN>], [<COLUMN_3>]],

    // Rename before merging when both tables share a generic name such as "Name"
    RightRenamed = Table.RenameColumns(RightTable, {{"<COLUMN_3>", "<NEW_COLUMN_NAME>"}}),

    Merged = Table.NestedJoin(
        LeftTable,    {"<KEY_COLUMN>"},
        RightRenamed, {"<KEY_COLUMN>"},
        "Joined",
        JoinKind.LeftOuter            // Inner, LeftOuter, RightOuter, FullOuter, LeftAnti, RightAnti
    ),

    Expanded = Table.ExpandTableColumn(Merged, "Joined", {"<NEW_COLUMN_NAME>"}, {"<NEW_COLUMN_NAME>"})
in
    Expanded


// =====================================================================
// 4) Power Platform / Power BI dataflow entity
// ---------------------------------------------------------------------
// Navigating by workspaceId/dataflowId (instead of by display name) keeps the
// query working if the workspace or dataflow is renamed.
// =====================================================================
let
    Source     = PowerPlatform.Dataflows(null),
    Workspaces = Source{[Id = "Workspaces"]}[Data],
    Workspace  = Workspaces{[workspaceId = WorkspaceId]}[Data],
    Dataflow   = Workspace{[dataflowId = DataflowId]}[Data],
    Entity     = Dataflow{[entity = "<TABLE>", version = ""]}[Data]
in
    Entity
