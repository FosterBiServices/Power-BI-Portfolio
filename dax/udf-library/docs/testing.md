# Testing Checklist

- Confirm the semantic model compatibility level supports DAX UDFs.
- Confirm the date table has one row per date and no gaps.
- Test completed and partial year, quarter, and month contexts.
- Test month-end, quarter-end, year-end, and leap-day behavior.
- Test zero and blank prior values for all growth functions.
- Test PP and POP at year, quarter, month, and card scope.
- Compare each UDF result with a manually verified measure.
- Confirm totals behave as documented.
