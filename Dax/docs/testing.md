# Pattern Testing

Test each pattern with a small, independently verifiable base measure.

## Required checks

1. Confirm the date table contains one row per date with no gaps.
2. Confirm the date column is used by the active relationship to the fact table.
3. Test a completed year, quarter, and month.
4. Test a partial year, quarter, and month.
5. Test a leap year and a month-end boundary.
6. Test a zero prior value and a blank prior value.
7. Test row-level results and the visual grand total.
8. For PP and POP, test year, quarter, month, and card contexts.
9. For complete-period patterns, apply a current-period slicer and verify that the prior complete period still resolves.
10. Record the expected and actual result in the pull request.
