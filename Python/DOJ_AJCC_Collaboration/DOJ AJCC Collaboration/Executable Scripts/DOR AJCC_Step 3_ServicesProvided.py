
import pandas as pd

# File path supplied by Power Query
input_path = FilePath.iloc[0, 0]


# Region-code lookup
_regionLookup = {
  "Sacramento Employment and Training Agency": 29,
  "Workforce Investment Board of Solano County": 43,
  "Workforce Development Board of Ventura County": 48,
  "North Central Counties Consortium": 23,
  "Southeast Los Angeles Workforce Development Board": 42,
  "Workforce Development Board of Madera County": 15,
  "San Bernardino County Workforce Development Department": 32,
  "City of Los Angeles Workforce Development Board": 12,
  "Golden Sierra Workforce Development Board": 7,
  "Yolo County Health and Human Services Agency (HHSA)": 50,
  "Humboldt County Workforce Development Board": 8,
  "South Bay Workforce Investment Board": 45,
  "San Joaquin County Workforce Development Board": 35,
  "Alameda County Workforce Development Board": 1,
  "Mother Lode Workforce Development Board": 20,
  "NoRTEC - Northern Rural Training & Employment Consortium": 22,
  "Riverside County Workforce Development Division": 28,
  "San Diego Workforce Partnership, Inc.": 33
}


# Normalize matching values without changing displayed values
def normalize_key(_value):
  if pd.isna(_value):
    return None

  return " ".join(
    str(_value)
    .replace("\n", " ")
    .split()
  ).casefold()


# Create a normalized region lookup
_regionByKey = {
  normalize_key(_region): _code
  for _region, _code in _regionLookup.items()
}


# Load the first worksheet without predefined headers
try:
  _raw = pd.read_excel(
    input_path,
    sheet_name=0,
    header=None,
    engine="openpyxl"
  )
except Exception as _error:
  raise RuntimeError(
    f"Unable to read the Excel workbook: {input_path}. "
    f"Original error: {_error}"
  ) from _error


# Validate that the worksheet contains data
if _raw.empty:
  raise ValueError(
    f"The first worksheet in {input_path} contains no data."
  )

if _raw.shape[1] < 1:
  raise ValueError(
    "The first worksheet does not contain any usable columns."
  )


# Locate the header row using User ID in the first column
_headerMatches = _raw.index[
  _raw.iloc[:, 0]
  .astype("string")
  .str.strip()
  .str.casefold()
  .eq("user id")
]


if _headerMatches.empty:
  raise ValueError(
    "A header row containing 'User ID' was not found "
    "in the first column of the first worksheet."
  )

_headerIndex = _headerMatches[0]


# Remove report content above the detected header
_clean = (
  _raw
  .iloc[_headerIndex:]
  .reset_index(drop=True)
  .copy()
)


# Promote the detected row to headers
_clean.columns = _clean.iloc[0]

_clean = (
  _clean
  .iloc[1:]
  .reset_index(drop=True)
  .copy()
)


# Clean headers and safely handle blank or duplicate headers
_columnList = []
_columnCount = {}

for _index, _column in enumerate(_clean.columns):
  if pd.isna(_column):
    _name = ""
  else:
    _name = str(_column)

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


# Standardize the Region/LWDB field name
if "REGION/LWDB" in _clean.columns:
  _clean = _clean.rename(
    columns={
      "REGION/LWDB": "REGION LWDB"
    }
  )


# Required source fields
_stringFields = [
  "REGION LWDB",
  "OFFICE",
  "OFFICE OF RESPONSIBILITY",
  "SERVICE",
  "NAICS",
  "ONET",
  "COMPLETION STATUS",
  "PROGRAM",
  "PROVIDER",
  "REGISTERED APPRENTICESHIP",
  "TYPE OF APPRENTICESHIP",
  "HISPANIC",
  "LEARNING MODE",
  "AGENCY CODE",
  "EX OFFENDER",
  "COMMENTS"
]

_numericFields = [
  "USER ID",
  "STATE ID",
  "APP ID"
]

_dateFields = [
  "CREATE DATE",
  "ACTUAL BEGIN DATE",
  "PROJECTED BEGIN DATE",
  "ACTUAL END DATE",
  "PROJECTED END DATE",
  "MOST RECENT EMPLOYMENT DATE"
]

_requiredFields = (
  _stringFields
  + _numericFields
  + _dateFields
)

_missingFields = [
  _field
  for _field in _requiredFields
  if _field not in _clean.columns
]

if _missingFields:
  raise KeyError(
    "Required columns are missing after promoting and cleaning headers. "
    f"Missing columns: {_missingFields}. "
    f"Available columns: {_clean.columns.tolist()}"
  )


# Remove fully blank rows
_clean = (
  _clean
  .dropna(how="all")
  .copy()
)


# Remove repeated header rows embedded in the data
_clean = _clean[
  ~_clean["USER ID"]
  .astype("string")
  .str.strip()
  .str.casefold()
  .eq("user id")
].copy()


# Remove total rows
_clean = _clean[
  ~_clean["USER ID"]
  .astype("string")
  .str.contains(
    "total",
    case=False,
    na=False,
    regex=False
  )
].copy()


# Convert and clean expected text fields
for _field in _stringFields:
  _clean[_field] = (
    _clean[_field]
    .astype("string")
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
  )


# Validate and convert expected numeric fields
for _field in _numericFields:
  _original = _clean[_field]

  # Treat empty text as missing rather than invalid
  _blank = (
    _original
    .astype("string")
    .str.strip()
    .eq("")
  )

  _converted = pd.to_numeric(
    _original.mask(_blank),
    errors="coerce"
  )

  _invalid = (
    _converted.isna()
    & _original.notna()
    & ~_blank
  )

  if _invalid.any():
    _invalidValues = (
      _original.loc[_invalid]
      .astype("string")
      .drop_duplicates()
      .head(10)
      .tolist()
    )

    raise TypeError(
      f"Column '{_field}' contains nonnumeric data. "
      f"Example invalid values: {_invalidValues}"
    )

  _clean[_field] = _converted


# Use nullable whole numbers for identifier fields
for _field in _numericFields:
  _fractional = (
    _clean[_field].notna()
    & (_clean[_field] % 1 != 0)
  )

  if _fractional.any():
    _fractionalValues = (
      _clean.loc[_fractional, _field]
      .drop_duplicates()
      .head(10)
      .tolist()
    )

    raise ValueError(
      f"Column '{_field}' contains decimal values but is expected "
      f"to contain whole-number identifiers. "
      f"Example invalid values: {_fractionalValues}"
    )

  _clean[_field] = _clean[_field].astype("Int64")


# Validate and convert expected date fields
for _field in _dateFields:
  _original = _clean[_field]

  _blank = (
    _original
    .astype("string")
    .str.strip()
    .eq("")
  )

  _converted = pd.to_datetime(
    _original.mask(_blank),
    errors="coerce"
  )

  _invalid = (
    _converted.isna()
    & _original.notna()
    & ~_blank
  )

  if _invalid.any():
    _invalidValues = (
      _original.loc[_invalid]
      .astype("string")
      .drop_duplicates()
      .head(10)
      .tolist()
    )

    raise TypeError(
      f"Column '{_field}' contains invalid date values. "
      f"Example invalid values: {_invalidValues}"
    )

  _clean[_field] = _converted


# Apply proper case only to fields where case normalization is intended
_properCaseFields = [
  "OFFICE",
  "OFFICE OF RESPONSIBILITY",
  "SERVICE",
  "NAICS",
  "ONET",
  "COMPLETION STATUS",
  "PROGRAM",
  "PROVIDER",
  "REGISTERED APPRENTICESHIP",
  "TYPE OF APPRENTICESHIP",
  "HISPANIC",
  "LEARNING MODE",
  "EX OFFENDER",
  "COMMENTS"
]

for _field in _properCaseFields:
  _clean[_field] = (
    _clean[_field]
    .astype("string")
    .str.strip()
    .str.title()
  )


# Agency Code should remain uppercase
_clean["AGENCY CODE"] = (
  _clean["AGENCY CODE"]
  .astype("string")
  .str.strip()
  .str.upper()
)


# Define the aggregation grain
_groupFields = [
  "REGION LWDB",
  "OFFICE",
  "OFFICE OF RESPONSIBILITY",
  "SERVICE",
  "NAICS",
  "ONET",
  "COMPLETION STATUS",
  "PROGRAM",
  "PROVIDER",
  "REGISTERED APPRENTICESHIP",
  "TYPE OF APPRENTICESHIP",
  "HISPANIC",
  "LEARNING MODE",
  "AGENCY CODE",
  "EX OFFENDER",
  "COMMENTS",
  "CREATE DATE",
  "ACTUAL BEGIN DATE",
  "PROJECTED BEGIN DATE",
  "ACTUAL END DATE",
  "PROJECTED END DATE",
  "MOST RECENT EMPLOYMENT DATE"
]


# Aggregate the number of populated User ID records
Result = (
  _clean
  .groupby(
    _groupFields,
    as_index=False,
    dropna=False
  )
  .agg(
    {
      "USER ID": "count"
    }
  )
  .rename(
    columns={
      "USER ID": "USER ID COUNT"
    }
  )
)


# Remove groups without a populated User ID
Result = (
  Result[
    Result["USER ID COUNT"] > 0
  ]
  .reset_index(drop=True)
)


# Map region codes using normalized keys
Result["REGION CODE"] = (
  Result["REGION LWDB"]
  .map(normalize_key)
  .map(_regionByKey)
  .astype("Int64")
)


# Validate region mappings
_unmappedMask = (
  Result["REGION LWDB"].notna()
  & Result["REGION CODE"].isna()
)

if _unmappedMask.any():
  _unmappedRegions = (
    Result.loc[
      _unmappedMask,
      "REGION LWDB"
    ]
    .astype("string")
    .drop_duplicates()
    .sort_values()
    .tolist()
  )

  raise ValueError(
    "One or more REGION LWDB values do not have a matching "
    "REGION CODE. "
    f"Unmapped regions: {_unmappedRegions}"
  )


# Reinforce the resulting count data type
Result["USER ID COUNT"] = (
  Result["USER ID COUNT"]
  .astype("Int64")
)


# Put Region Code next to the region description
_outputFields = [
  "REGION LWDB",
  "REGION CODE",
  "OFFICE",
  "OFFICE OF RESPONSIBILITY",
  "SERVICE",
  "NAICS",
  "ONET",
  "COMPLETION STATUS",
  "PROGRAM",
  "PROVIDER",
  "REGISTERED APPRENTICESHIP",
  "TYPE OF APPRENTICESHIP",
  "HISPANIC",
  "LEARNING MODE",
  "AGENCY CODE",
  "EX OFFENDER",
  "COMMENTS",
  "CREATE DATE",
  "ACTUAL BEGIN DATE",
  "PROJECTED BEGIN DATE",
  "ACTUAL END DATE",
  "PROJECTED END DATE",
  "MOST RECENT EMPLOYMENT DATE",
  "USER ID COUNT"
]

Result = Result[_outputFields].copy()


