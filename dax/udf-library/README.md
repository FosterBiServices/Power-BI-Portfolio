# DAX Time Intelligence UDF Library

A Git-ready collection of reusable DAX user-defined functions. The functions accept the calculation expression, date table, and date column as arguments, so no physical table or measure names are embedded in the library.

## Distributions

- `distribution/all-functions.dax`: Query-view `DEFINE FUNCTION` definitions for testing and model updates.
- `distribution/functions.tmdl`: Model-level function definitions for a PBIP `definition/functions.tmdl` file.
- `functions/`: One reviewable `.dax` file per function.

## Standard call

```DAX
CPT Code Distribution Value YTD =
  YearToDate(
    [CPT Code Distribution Value],
    'dimDates',
    'dimDates'[DateValue]
  )
```

Dynamic functions also receive hierarchy columns:

```DAX
CPT Code Distribution Value PP =
  PriorPeriod(
    [CPT Code Distribution Value],
    'dimDates',
    'dimDates'[DateValue],
    'dimDates'[Year],
    'dimDates'[Quarter],
    'dimDates'[Month]
  )
```

## Assumptions

- Calendar-year logic is used for complete year and quarter patterns.
- MAT is an inclusive trailing 12-month period ending on the latest visible date.
- Growth functions return `(current - prior) / prior` through `DIVIDE`.
- PP and POP return blank when year, quarter, or month is not in hierarchy scope.
- The date table contains a continuous date column and is marked as a date table.

## Git workflow

1. Edit a single function file.
2. Update the matching entry in both distribution files.
3. Run the checks in `docs/testing.md`.
4. Update `CHANGELOG.md` and `VERSION` for released behavior changes.
5. Submit a pull request with expected and actual test results.
