import pandas as pd
from pathlib import Path


input_path = FilePath.iloc[0, 0]

# Read the first worksheet without promoting headers
try:
  _raw = pd.read_excel(
    input_path,
    sheet_name=0,
    header=None,
    engine="openpyxl"
  )
except Exception as _error:
  raise RuntimeError(
    f"Unable to read the Excel file: {input_path}. "
    f"Original error: {_error}"
  ) from _error


# Validate that the workbook contains at least two columns
if _raw.shape[1] < 2:
  raise ValueError(
    "The selected worksheet contains fewer than two columns. "
    "The script expects 'Grant' to appear in the second column."
  )


# Locate the header row by finding Grant in the second column
_headerMatches = _raw.index[
  _raw.iloc[:, 1]
  .astype("string")
  .str.strip()
  .str.casefold()
  .eq("grant")
]


if _headerMatches.empty:
  raise ValueError(
    "A header row containing 'Grant' was not found "
    "in the second column of the first worksheet."
  )


_headerIndex = _headerMatches[0]


# Remove report content above the detected header
_clean = (
  _raw
  .iloc[_headerIndex:]
  .reset_index(drop=True)
  .copy()
)


# Promote the detected row to column headers
_clean.columns = _clean.iloc[0]

_clean = (
  _clean
  .iloc[1:]
  .reset_index(drop=True)
  .copy()
)


# Standardize column names and safely handle blank headers
_columnList = []
_columnCount = {}

for _index, _column in enumerate(_clean.columns):
  # Convert null headers to an empty string before cleaning
  if pd.isna(_column):
    _name = ""
  else:
    _name = str(_column)

  # Remove line breaks, collapse whitespace, trim, and capitalize
  _name = (
    _name
    .replace("\n", " ")
    .strip()
    .upper()
  )

  _name = " ".join(_name.split())

  # Assign a safe name to blank Excel headers
  if not _name:
    _name = f"UNNAMED COLUMN {_index + 1}"

  # Ensure every column name is unique
  if _name in _columnCount:
    _columnCount[_name] += 1
    _name = f"{_name} {_columnCount[_name]}"
  else:
    _columnCount[_name] = 1

  _columnList.append(_name)

_clean.columns = _columnList


# Detect blank or duplicate column names
if _clean.columns.isna().any() or (_clean.columns == "").any():
  raise ValueError(
    "One or more columns have a blank header after cleaning."
  )

if _clean.columns.duplicated().any():
  _duplicates = (
    _clean.columns[_clean.columns.duplicated()]
    .unique()
    .tolist()
  )

  raise ValueError(
    f"Duplicate column names were found after cleaning: {_duplicates}"
  )


# Validate required fields before referencing them
_required = [
  "GRANT",
  "LWDB",
  "APP ID",
  "RESPONSIBLE OFFICE",
  "PARTICIPATION DATE",
  "GRANT ENROLL DATE",
  "LAST GRANT ACTIVITY DATE",
  "PROJECTED GRANT ACTIVITY END DATE",
  "EXIT DATE",
  "RECEIVED CREDENTIAL",
  "ENTERED EMPLOYMENT",
  "WITH DISABILITY"
]

_missing = [
  _column
  for _column in _required
  if _column not in _clean.columns
]

if _missing:
  raise KeyError(
    f"Required columns are missing from the source file: {_missing}"
  )


# Remove fully blank rows
_clean = (
  _clean
  .dropna(how="all")
  .copy()
)


# Remove repeated embedded header rows
_clean = _clean[
  ~_clean["GRANT"]
  .astype("string")
  .str.strip()
  .str.casefold()
  .eq("grant")
].copy()


# Remove total rows
_clean = _clean[
  ~_clean["GRANT"]
  .astype("string")
  .str.contains(
    "total",
    case=False,
    na=False,
    regex=False
  )
].copy()


# Convert LWDB to a nullable whole-number field
try:
  _clean["LWDB"] = (
    pd.to_numeric(
      _clean["LWDB"],
      errors="raise"
    )
    .astype("Int64")
  )
except (TypeError, ValueError) as _error:
  _invalidLwdb = (
    _clean.loc[
      pd.to_numeric(
        _clean["LWDB"],
        errors="coerce"
      ).isna()
      & _clean["LWDB"].notna(),
      "LWDB"
    ]
    .astype("string")
    .drop_duplicates()
    .tolist()
  )

  raise ValueError(
    "LWDB contains values that cannot be converted to whole numbers. "
    f"Invalid values: {_invalidLwdb}"
  ) from _error


# Select fields used by the aggregation
_fields = [
  "LWDB",
  "APP ID",
  "RESPONSIBLE OFFICE",
  "PARTICIPATION DATE",
  "GRANT ENROLL DATE",
  "LAST GRANT ACTIVITY DATE",
  "PROJECTED GRANT ACTIVITY END DATE",
  "EXIT DATE",
  "RECEIVED CREDENTIAL",
  "ENTERED EMPLOYMENT",
  "WITH DISABILITY"
]

_selected = _clean[_fields].copy()


# Define the grouping grain
_groups = [
  "LWDB",
  "RESPONSIBLE OFFICE",
  "PARTICIPATION DATE",
  "GRANT ENROLL DATE",
  "LAST GRANT ACTIVITY DATE",
  "PROJECTED GRANT ACTIVITY END DATE",
  "EXIT DATE",
  "RECEIVED CREDENTIAL",
  "ENTERED EMPLOYMENT",
  "WITH DISABILITY"
]


# Aggregate the number of nonblank APP ID values
Result = (
  _selected
  .groupby(
    _groups,
    as_index=False,
    dropna=False
  )
  .agg(
    {
      "APP ID": "count"
    }
  )
  .rename(
    columns={
      "APP ID": "APP ID COUNT"
    }
  )
)


# Remove groups without a populated APP ID
Result = (
  Result[
    Result["APP ID COUNT"] > 0
  ]
  .reset_index(drop=True)
)


# Reinforce output data types
Result["LWDB"] = Result["LWDB"].astype("Int64")
Result["APP ID COUNT"] = Result["APP ID COUNT"].astype("Int64")