string.Join(",\r\n", 
    Selected.Table.DataColumns
        .OrderBy(c => c.SourceColumn)
        .Select(c => "[" + c.SourceColumn + "]")
    ).Output();
