# # Grant Enrollments File Validation Review
# 
# ## Purpose
# 
# This notebook validates all source files required for the Grant Enrollments Power BI reporting solution before a dataset refresh is performed.
# 
# The objective is to ensure incoming files meet the required structural and data quality standards and do not introduce refresh failures, data integrity issues, or inaccurate reporting results.
# 
# ## Files Reviewed
# 
# | File | Purpose |
# |--------|--------|
# | Regions.xlsx | Regional reference data used for lookup relationships |
# | Grant Enrollments_GrantParticipants.xlsx | Participant-level grant activity data |
# | Grant Enrollments_ServicesProvided.xlsx | Service-level activity and outcome data |
# 
# ## Validation Categories
# 
# The following validations are performed on each file:
# 
# - Required column validation
# - Unexpected column detection
# - Required field validation
# - Integer data type validation
# - Date data type validation
# - String field validation
# - Duplicate record detection
# - Uniqueness key enforcement
# 
# ## Success Criteria
# 
# A file is considered **Ready for Refresh** when:
# 
# - All required columns exist
# - No unexpected columns are present
# - Required fields contain data
# - Data types match expected definitions
# - No duplicate business keys exist
# 
# Any validation failure should be reviewed and corrected before Power BI data refresh activities proceed.

# In[ ]:





# In[10]:


import pandas as pd
import numpy as np
from pathlib import Path

# Update this path if needed
DATA_DIR = Path( r"C:\Users\<USER>\Downloads\Grant Enrollments")

regions = pd.read_excel(DATA_DIR / 'Regions.xlsx')
participants = pd.read_excel(DATA_DIR / 'GrantEnrollments_GrantParticipants.xlsx')
services = pd.read_excel(DATA_DIR / 'GrantEnrollments_SevicesProvided.xlsx')

participants.head()


# In[ ]:





# # Regions File Validation
# 
# ## Business Purpose
# 
# The Regions file serves as a reference table used throughout the reporting model to support regional mappings and reporting relationships.
# 
# Because this file functions as a lookup table, duplicate or invalid records can cause relationship issues within Power BI and impact report accuracy.
# 
# ## Validation Rules
# 
# | Validation | Requirement |
# |------------|-------------|
# | Required Columns | All expected columns must exist |
# | Nullable Fields | No nullable fields permitted |
# | Region Code | Must contain valid integer values |
# | Region Attributes | Must contain valid text values |
# | Duplicate Records | Combination of business key fields must be unique |
# 
# ## Expected Result
# 
# The file should contain a single unique record for each region and pass all structural validation checks before refresh.
# 

# In[ ]:





# In[1]:


import pandas as pd
import numpy as np


# =============================
# VALIDATION CONFIGURATION
# =============================

EXPECTED_COLUMNS = [
    "REGION LWDB",
    "REGION CODE",
    "REGION SHORT ABBR"
]

NULLABLE_COLUMNS = []

REQUIRED_NON_NULL = [
    column
    for column in EXPECTED_COLUMNS
    if column not in NULLABLE_COLUMNS
]

INTEGER_COLUMNS = [
    "REGION CODE"
]

DATE_COLUMNS = []

STRING_COLUMNS = [
    "REGION LWDB",
    "REGION SHORT ABBR"
]

UNIQUENESS_KEYS = [
    "REGION LWDB",
    "REGION CODE",
    "REGION SHORT ABBR"
]


# =============================
# HELPER FUNCTIONS
# =============================

def is_blank_series(series: pd.Series) -> pd.Series:
    return (
        series
        .replace("", np.nan)
        .replace(" ", np.nan)
        .isna()
    )


def print_rows(rows: pd.DataFrame) -> None:
    try:
        display(rows)
    except NameError:
        print(rows)


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df.columns = [
        str(column).strip().upper()
        for column in df.columns
    ]

    return df


def get_available_columns(df: pd.DataFrame, columns: list) -> list:
    return [
        column
        for column in columns
        if column in df.columns
    ]


def validate_integer_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    validation_df = df.copy()

    value_as_string = (
        validation_df[column]
        .astype("string")
        .str.strip()
    )

    is_blank = is_blank_series(validation_df[column])

    numeric_value = pd.to_numeric(
        value_as_string,
        errors="coerce"
    )

    has_decimal_value = (
        numeric_value.notna()
        & (numeric_value % 1 != 0)
    )

    invalid_integer = (
        ~is_blank
        & (
            numeric_value.isna()
            | has_decimal_value
        )
    )

    return validation_df.loc[
        invalid_integer,
        [column]
    ]


def validate_date_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    validation_df = df.copy()

    is_blank = is_blank_series(validation_df[column])

    parsed_date = pd.to_datetime(
        validation_df[column],
        errors="coerce"
    )

    invalid_date = (
        ~is_blank
        & parsed_date.isna()
    )

    return validation_df.loc[
        invalid_date,
        [column]
    ]


def validate_string_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    validation_df = df.copy()

    value_as_string = (
        validation_df[column]
        .astype("string")
        .str.strip()
    )

    is_blank = is_blank_series(validation_df[column])

    invalid_string = (
        ~is_blank
        & value_as_string.isna()
    )

    return validation_df.loc[
        invalid_string,
        [column]
    ]


# =============================
# VALIDATION LOGIC
# =============================

def validate_excel(df: pd.DataFrame) -> dict:
    report = {
        "missing_columns": [],
        "unexpected_columns": [],
        "null_violations": {},
        "integer_violations": {},
        "date_violations": {},
        "string_violations": {},
        "duplicate_key_violations": pd.DataFrame(),
        "row_count": len(df)
    }

    df = normalize_column_names(df)

    actual_columns = list(df.columns)

    report["missing_columns"] = [
        column
        for column in EXPECTED_COLUMNS
        if column not in actual_columns
    ]

    report["unexpected_columns"] = [
        column
        for column in actual_columns
        if column not in EXPECTED_COLUMNS
    ]

    available_expected_columns = get_available_columns(
        df,
        EXPECTED_COLUMNS
    )

    # Only validate columns that actually exist.
    # Missing columns are already captured above.
    for column in get_available_columns(df, REQUIRED_NON_NULL):
        blank_rows = df.loc[
            is_blank_series(df[column]),
            available_expected_columns
        ]

        if not blank_rows.empty:
            report["null_violations"][column] = blank_rows

    for column in get_available_columns(df, INTEGER_COLUMNS):
        invalid_rows = validate_integer_column(df, column)

        if not invalid_rows.empty:
            report["integer_violations"][column] = df.loc[
                invalid_rows.index,
                available_expected_columns
            ]

    for column in get_available_columns(df, DATE_COLUMNS):
        invalid_rows = validate_date_column(df, column)

        if not invalid_rows.empty:
            report["date_violations"][column] = df.loc[
                invalid_rows.index,
                available_expected_columns
            ]

    for column in get_available_columns(df, STRING_COLUMNS):
        invalid_rows = validate_string_column(df, column)

        if not invalid_rows.empty:
            report["string_violations"][column] = df.loc[
                invalid_rows.index,
                available_expected_columns
            ]

    available_uniqueness_keys = get_available_columns(
        df,
        UNIQUENESS_KEYS
    )

    if len(available_uniqueness_keys) == len(UNIQUENESS_KEYS):
        duplicate_rows = df.loc[
            df.duplicated(
                subset=UNIQUENESS_KEYS,
                keep=False
            ),
            available_expected_columns
        ]

        if not duplicate_rows.empty:
            report["duplicate_key_violations"] = (
                duplicate_rows
                .sort_values(by=UNIQUENESS_KEYS)
            )

    return report


# =============================
# REPORT PRINTING
# =============================

def print_report(report: dict) -> None:
    print("=== Data Quality Report ===\n")

    print(f"Rows Reviewed: {report['row_count']}\n")

    if report["missing_columns"]:
        print("Missing Columns:")
        for column in report["missing_columns"]:
            print(f"  - {column}")
        print()
    else:
        print("Missing Columns: None\n")

    if report["unexpected_columns"]:
        print("Unexpected Columns:")
        for column in report["unexpected_columns"]:
            print(f"  - {column}")
        print()
    else:
        print("Unexpected Columns: None\n")

    if report["null_violations"]:
        print("Non-Nullable Column Violations:")
        for column, rows in report["null_violations"].items():
            print(f"\nColumn: {column}")
            print(f"Invalid Rows: {len(rows)}")
            print_rows(rows)
        print()
    else:
        print("Non-Nullable Column Violations: None\n")

    if report["integer_violations"]:
        print("Integer Validation Violations:")
        for column, rows in report["integer_violations"].items():
            print(f"\nColumn: {column}")
            print(f"Invalid Rows: {len(rows)}")
            print_rows(rows)
        print()
    else:
        print("Integer Validation Violations: None\n")

    if report["date_violations"]:
        print("Date Validation Violations:")
        for column, rows in report["date_violations"].items():
            print(f"\nColumn: {column}")
            print(f"Invalid Rows: {len(rows)}")
            print_rows(rows)
        print()
    else:
        print("Date Validation Violations: None\n")

    if report["string_violations"]:
        print("String Validation Violations:")
        for column, rows in report["string_violations"].items():
            print(f"\nColumn: {column}")
            print(f"Invalid Rows: {len(rows)}")
            print_rows(rows)
        print()
    else:
        print("String Validation Violations: None\n")

    if not report["duplicate_key_violations"].empty:
        print("Duplicate Uniqueness Key Violations:")
        print(f"Uniqueness Key: {', '.join(UNIQUENESS_KEYS)}")
        print(f"Invalid Rows: {len(report['duplicate_key_violations'])}")
        print_rows(report["duplicate_key_violations"])
        print()
    else:
        print("Duplicate Uniqueness Key Violations: None\n")

    has_errors = (
        len(report["missing_columns"]) > 0
        or len(report["unexpected_columns"]) > 0
        or len(report["null_violations"]) > 0
        or len(report["integer_violations"]) > 0
        or len(report["date_violations"]) > 0
        or len(report["string_violations"]) > 0
        or not report["duplicate_key_violations"].empty
    )

    if has_errors:
        print("Validation Result: ❌ FAILED")
    else:
        print("Validation Result: ✅ PASSED")


# =============================
# EXCEL FILE PATH GOES HERE
# =============================

file_path = (
    r"C:\Users\<USER>\<COMPANY>\<PARENT>"
    r"\Power BI Source Files\Grant Enrollments\Regions.xlsx"
)


# =============================
# READ EXCEL
# =============================

df = pd.read_excel(
    file_path,
    dtype="string"
)


# =============================
# RUN VALIDATION
# =============================

report = validate_excel(df)

print_report(report)


# In[ ]:





# # Participant File Validation
# 
# ## Business Purpose
# 
# The Participants file contains grant participant enrollment, activity, exit, and outcome information used for participant reporting and performance measurement.
# 
# Data quality issues within this file may impact:
# 
# - Participant counts
# - Employment outcomes
# - Credential attainment metrics
# - Grant performance reporting
# 
# ## Validation Rules
# 
# ### Required Fields
# 
# The following fields must contain values:
# 
# - LWDB
# - Responsible Office
# - Participation Date
# - Grant Enroll Date
# - Received Credential
# - Entered Employment
# - With Disability
# - App ID
# 
# ### Optional Fields
# 
# The following fields may be blank:
# 
# - Last Grant Activity Date
# - Projected Grant Activity End Date
# - Exit Date
# 
# ### Data Type Validation
# 
# | Field Type | Validation |
# |------------|------------|
# | Integer | LWDB, App ID |
# | Date | All date columns |
# | Text | Office and indicator fields |
# 
# ### Duplicate Validation
# 
# Records must remain unique across the defined business key to prevent participant duplication within reporting outputs.
# 

# In[ ]:





# In[2]:


import pandas as pd
import numpy as np


# =============================
# VALIDATION CONFIGURATION
# =============================

EXPECTED_COLUMNS = [
    "LWDB",
    "RESPONSIBLE OFFICE",
    "PARTICIPATION DATE",
    "GRANT ENROLL DATE",
    "LAST GRANT ACTIVITY DATE",
    "PROJECTED GRANT ACTIVITY END DATE",
    "EXIT DATE",
    "RECEIVED CREDENTIAL",
    "ENTERED EMPLOYMENT",
    "WITH DISABILITY",
    "APP ID"
]

NULLABLE_COLUMNS = [
    "LAST GRANT ACTIVITY DATE",
    "PROJECTED GRANT ACTIVITY END DATE",
    "EXIT DATE"
]

REQUIRED_NON_NULL = [
    column
    for column in EXPECTED_COLUMNS
    if column not in NULLABLE_COLUMNS
]

INTEGER_COLUMNS = [
    "LWDB",
    "APP ID"
]

DATE_COLUMNS = [
    "PARTICIPATION DATE",
    "GRANT ENROLL DATE",
    "LAST GRANT ACTIVITY DATE",
    "PROJECTED GRANT ACTIVITY END DATE",
    "EXIT DATE"
]

STRING_COLUMNS = [
    "RESPONSIBLE OFFICE",
    "RECEIVED CREDENTIAL",
    "ENTERED EMPLOYMENT",
    "WITH DISABILITY"
]

UNIQUENESS_KEYS = [
    "LWDB",
    "PARTICIPATION DATE",
    "GRANT ENROLL DATE",
    "LAST GRANT ACTIVITY DATE",
    "PROJECTED GRANT ACTIVITY END DATE",
    "EXIT DATE"
    "RESPONSIBLE OFFICE",
    "RECEIVED CREDENTIAL",
    "ENTERED EMPLOYMENT",
    "WITH DISABILITY"
]


# =============================
# HELPER FUNCTIONS
# =============================

def is_blank_series(series: pd.Series) -> pd.Series:
    return (
        series
        .replace("", np.nan)
        .replace(" ", np.nan)
        .isna()
    )


def print_rows(rows: pd.DataFrame) -> None:
    try:
        display(rows)
    except NameError:
        print(rows)


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df.columns = [
        str(column).strip().upper()
        for column in df.columns
    ]

    return df


def get_available_columns(df: pd.DataFrame, columns: list) -> list:
    return [
        column
        for column in columns
        if column in df.columns
    ]


def validate_integer_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    validation_df = df.copy()

    value_as_string = (
        validation_df[column]
        .astype("string")
        .str.strip()
    )

    is_blank = is_blank_series(validation_df[column])

    numeric_value = pd.to_numeric(
        value_as_string,
        errors="coerce"
    )

    has_decimal_value = (
        numeric_value.notna()
        & (numeric_value % 1 != 0)
    )

    invalid_integer = (
        ~is_blank
        & (
            numeric_value.isna()
            | has_decimal_value
        )
    )

    return validation_df.loc[
        invalid_integer,
        [column]
    ]


def validate_date_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    validation_df = df.copy()

    is_blank = is_blank_series(validation_df[column])

    parsed_date = pd.to_datetime(
        validation_df[column],
        errors="coerce"
    )

    invalid_date = (
        ~is_blank
        & parsed_date.isna()
    )

    return validation_df.loc[
        invalid_date,
        [column]
    ]


def validate_string_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    validation_df = df.copy()

    is_blank = is_blank_series(validation_df[column])

    invalid_string = (
        ~is_blank
        & validation_df[column].isna()
    )

    return validation_df.loc[
        invalid_string,
        [column]
    ]


# =============================
# VALIDATION LOGIC
# =============================

def validate_excel(df: pd.DataFrame) -> dict:
    report = {
        "missing_columns": [],
        "unexpected_columns": [],
        "null_violations": {},
        "integer_violations": {},
        "date_violations": {},
        "string_violations": {},
        "duplicate_key_violations": pd.DataFrame(),
        "row_count": len(df)
    }

    df = normalize_column_names(df)

    actual_columns = list(df.columns)

    report["missing_columns"] = [
        column
        for column in EXPECTED_COLUMNS
        if column not in actual_columns
    ]

    report["unexpected_columns"] = [
        column
        for column in actual_columns
        if column not in EXPECTED_COLUMNS
    ]

    available_expected_columns = get_available_columns(
        df,
        EXPECTED_COLUMNS
    )

    # Only validate columns that actually exist.
    # Missing columns are already captured above.
    for column in get_available_columns(df, REQUIRED_NON_NULL):
        blank_rows = df.loc[
            is_blank_series(df[column]),
            available_expected_columns
        ]

        if not blank_rows.empty:
            report["null_violations"][column] = blank_rows

    for column in get_available_columns(df, INTEGER_COLUMNS):
        invalid_rows = validate_integer_column(df, column)

        if not invalid_rows.empty:
            report["integer_violations"][column] = df.loc[
                invalid_rows.index,
                available_expected_columns
            ]

    for column in get_available_columns(df, DATE_COLUMNS):
        invalid_rows = validate_date_column(df, column)

        if not invalid_rows.empty:
            report["date_violations"][column] = df.loc[
                invalid_rows.index,
                available_expected_columns
            ]

    for column in get_available_columns(df, STRING_COLUMNS):
        invalid_rows = validate_string_column(df, column)

        if not invalid_rows.empty:
            report["string_violations"][column] = df.loc[
                invalid_rows.index,
                available_expected_columns
            ]

    available_uniqueness_keys = get_available_columns(
        df,
        UNIQUENESS_KEYS
    )

    if len(available_uniqueness_keys) == len(UNIQUENESS_KEYS):
        duplicate_rows = df.loc[
            df.duplicated(
                subset=UNIQUENESS_KEYS,
                keep=False
            ),
            available_expected_columns
        ]

        if not duplicate_rows.empty:
            report["duplicate_key_violations"] = (
                duplicate_rows
                .sort_values(by=UNIQUENESS_KEYS)
            )

    return report


# =============================
# REPORT PRINTING
# =============================

def print_report(report: dict) -> None:
    print("=== Data Quality Report ===\n")

    print(f"Rows Reviewed: {report['row_count']}\n")

    if report["missing_columns"]:
        print("Missing Columns:")
        for column in report["missing_columns"]:
            print(f"  - {column}")
        print()
    else:
        print("Missing Columns: None\n")

    if report["unexpected_columns"]:
        print("Unexpected Columns:")
        for column in report["unexpected_columns"]:
            print(f"  - {column}")
        print()
    else:
        print("Unexpected Columns: None\n")

    if report["null_violations"]:
        print("Non-Nullable Column Violations:")
        for column, rows in report["null_violations"].items():
            print(f"\nColumn: {column}")
            print(f"Invalid Rows: {len(rows)}")
            print_rows(rows)
        print()
    else:
        print("Non-Nullable Column Violations: None\n")

    if report["integer_violations"]:
        print("Integer Validation Violations:")
        for column, rows in report["integer_violations"].items():
            print(f"\nColumn: {column}")
            print(f"Invalid Rows: {len(rows)}")
            print_rows(rows)
        print()
    else:
        print("Integer Validation Violations: None\n")

    if report["date_violations"]:
        print("Date Validation Violations:")
        for column, rows in report["date_violations"].items():
            print(f"\nColumn: {column}")
            print(f"Invalid Rows: {len(rows)}")
            print_rows(rows)
        print()
    else:
        print("Date Validation Violations: None\n")

    if report["string_violations"]:
        print("String Validation Violations:")
        for column, rows in report["string_violations"].items():
            print(f"\nColumn: {column}")
            print(f"Invalid Rows: {len(rows)}")
            print_rows(rows)
        print()
    else:
        print("String Validation Violations: None\n")

    if not report["duplicate_key_violations"].empty:
        print("Duplicate Uniqueness Key Violations:")
        print(f"Uniqueness Key: {', '.join(UNIQUENESS_KEYS)}")
        print(f"Invalid Rows: {len(report['duplicate_key_violations'])}")
        print_rows(report["duplicate_key_violations"])
        print()
    else:
        print("Duplicate Uniqueness Key Violations: None\n")

    has_errors = (
        len(report["missing_columns"]) > 0
        or len(report["unexpected_columns"]) > 0
        or len(report["null_violations"]) > 0
        or len(report["integer_violations"]) > 0
        or len(report["date_violations"]) > 0
        or len(report["string_violations"]) > 0
        or not report["duplicate_key_violations"].empty
    )

    if has_errors:
        print("Validation Result: ❌ FAILED")
    else:
        print("Validation Result: ✅ PASSED")


# =============================
# EXCEL FILE PATH GOES HERE
# =============================

file_path = (
    r"C:\Users\<USER>\<COMPANY>\<PARENT>"
    r"\Power BI Source Files\Grant Enrollments\GrantEnrollments_GrantParticipants.xlsx"
)


# =============================
# READ EXCEL
# =============================

df = pd.read_excel(
    file_path,
    dtype="string"
)


# =============================
# RUN VALIDATION
# =============================

report = validate_excel(df)

print_report(report)


# In[ ]:





# # Services File Validation
# 
# ## Business Purpose
# 
# The Services file contains service delivery activity provided through AJCC programs.
# 
# This dataset supports operational reporting, workforce program analysis, service utilization tracking, and participant outcome monitoring.
# 
# Because this table contains transactional activity, data quality issues can significantly affect:
# 
# - Service counts
# - Program participation metrics
# - Workforce outcome reporting
# - Trend analysis
# 
# ## Validation Rules
# 
# ### Structural Validation
# 
# - Required fields must exist
# - No unexpected fields may be present
# 
# ### Data Quality Validation
# 
# The notebook validates:
# 
# - Required non-null fields
# - Integer fields
# - Date fields
# - String fields
# - Duplicate records
# 
# ### Business Key Validation
# 
# A uniqueness key is enforced to prevent duplicate service transactions from entering downstream reporting systems.

# In[ ]:





# In[3]:


import pandas as pd
import numpy as np


# =============================
# VALIDATION CONFIGURATION
# =============================

EXPECTED_COLUMNS = [
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
    "MOST RECENT EMPLOYMENT DATE",
    "USER ID",
    "REGION CODE"
]

NULLABLE_COLUMNS = [
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
    "PROJECTED BEGIN DATE",
    "ACTUAL END DATE",
    "PROJECTED END DATE",
    "MOST RECENT EMPLOYMENT DATE"
]

REQUIRED_NON_NULL = [
    column
    for column in EXPECTED_COLUMNS
    if column not in NULLABLE_COLUMNS
]

INTEGER_COLUMNS = [
    "USER ID",
    "REGION CODE"
]

DATE_COLUMNS = [
    "CREATE DATE",
    "ACTUAL BEGIN DATE",
    "PROJECTED BEGIN DATE",
    "ACTUAL END DATE",
    "PROJECTED END DATE",
    "MOST RECENT EMPLOYMENT DATE"
]

STRING_COLUMNS = [
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

UNIQUENESS_KEYS = [
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
    "MOST RECENT EMPLOYMENT DATE",
    "USER ID",
    "REGION CODE"
]


# =============================
# HELPER FUNCTIONS
# =============================

def is_blank_series(series: pd.Series) -> pd.Series:
    return (
        series
        .replace("", np.nan)
        .replace(" ", np.nan)
        .isna()
    )


def print_rows(rows: pd.DataFrame) -> None:
    try:
        display(rows)
    except NameError:
        print(rows)


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df.columns = [
        str(column).strip().upper()
        for column in df.columns
    ]

    return df


def get_available_columns(df: pd.DataFrame, columns: list) -> list:
    return [
        column
        for column in columns
        if column in df.columns
    ]


def validate_integer_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    validation_df = df.copy()

    value_as_string = (
        validation_df[column]
        .astype("string")
        .str.strip()
    )

    is_blank = is_blank_series(validation_df[column])

    numeric_value = pd.to_numeric(
        value_as_string,
        errors="coerce"
    )

    has_decimal_value = (
        numeric_value.notna()
        & (numeric_value % 1 != 0)
    )

    invalid_integer = (
        ~is_blank
        & (
            numeric_value.isna()
            | has_decimal_value
        )
    )

    return validation_df.loc[
        invalid_integer,
        [column]
    ]


def validate_date_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    validation_df = df.copy()

    is_blank = is_blank_series(validation_df[column])

    parsed_date = pd.to_datetime(
        validation_df[column],
        errors="coerce"
    )

    invalid_date = (
        ~is_blank
        & parsed_date.isna()
    )

    return validation_df.loc[
        invalid_date,
        [column]
    ]


def validate_string_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    validation_df = df.copy()

    value_as_string = (
        validation_df[column]
        .astype("string")
        .str.strip()
    )

    is_blank = is_blank_series(validation_df[column])

    invalid_string = (
        ~is_blank
        & value_as_string.isna()
    )

    return validation_df.loc[
        invalid_string,
        [column]
    ]


# =============================
# VALIDATION LOGIC
# =============================

def validate_excel(df: pd.DataFrame) -> dict:
    report = {
        "missing_columns": [],
        "unexpected_columns": [],
        "null_violations": {},
        "integer_violations": {},
        "date_violations": {},
        "string_violations": {},
        "duplicate_key_violations": pd.DataFrame(),
        "row_count": len(df)
    }

    df = normalize_column_names(df)

    actual_columns = list(df.columns)

    report["missing_columns"] = [
        column
        for column in EXPECTED_COLUMNS
        if column not in actual_columns
    ]

    report["unexpected_columns"] = [
        column
        for column in actual_columns
        if column not in EXPECTED_COLUMNS
    ]

    available_expected_columns = get_available_columns(
        df,
        EXPECTED_COLUMNS
    )

    # Only validate columns that actually exist.
    # Missing columns are already captured above.
    for column in get_available_columns(df, REQUIRED_NON_NULL):
        blank_rows = df.loc[
            is_blank_series(df[column]),
            available_expected_columns
        ]

        if not blank_rows.empty:
            report["null_violations"][column] = blank_rows

    for column in get_available_columns(df, INTEGER_COLUMNS):
        invalid_rows = validate_integer_column(df, column)

        if not invalid_rows.empty:
            report["integer_violations"][column] = df.loc[
                invalid_rows.index,
                available_expected_columns
            ]

    for column in get_available_columns(df, DATE_COLUMNS):
        invalid_rows = validate_date_column(df, column)

        if not invalid_rows.empty:
            report["date_violations"][column] = df.loc[
                invalid_rows.index,
                available_expected_columns
            ]

    for column in get_available_columns(df, STRING_COLUMNS):
        invalid_rows = validate_string_column(df, column)

        if not invalid_rows.empty:
            report["string_violations"][column] = df.loc[
                invalid_rows.index,
                available_expected_columns
            ]

    available_uniqueness_keys = get_available_columns(
        df,
        UNIQUENESS_KEYS
    )

    if len(available_uniqueness_keys) == len(UNIQUENESS_KEYS):
        duplicate_rows = df.loc[
            df.duplicated(
                subset=UNIQUENESS_KEYS,
                keep=False
            ),
            available_expected_columns
        ]

        if not duplicate_rows.empty:
            report["duplicate_key_violations"] = (
                duplicate_rows
                .sort_values(by=UNIQUENESS_KEYS)
            )

    return report


# =============================
# REPORT PRINTING
# =============================

def print_report(report: dict) -> None:
    print("=== Data Quality Report ===\n")

    print(f"Rows Reviewed: {report['row_count']}\n")

    if report["missing_columns"]:
        print("Missing Columns:")
        for column in report["missing_columns"]:
            print(f"  - {column}")
        print()
    else:
        print("Missing Columns: None\n")

    if report["unexpected_columns"]:
        print("Unexpected Columns:")
        for column in report["unexpected_columns"]:
            print(f"  - {column}")
        print()
    else:
        print("Unexpected Columns: None\n")

    if report["null_violations"]:
        print("Non-Nullable Column Violations:")
        for column, rows in report["null_violations"].items():
            print(f"\nColumn: {column}")
            print(f"Invalid Rows: {len(rows)}")
            print_rows(rows)
        print()
    else:
        print("Non-Nullable Column Violations: None\n")

    if report["integer_violations"]:
        print("Integer Validation Violations:")
        for column, rows in report["integer_violations"].items():
            print(f"\nColumn: {column}")
            print(f"Invalid Rows: {len(rows)}")
            print_rows(rows)
        print()
    else:
        print("Integer Validation Violations: None\n")

    if report["date_violations"]:
        print("Date Validation Violations:")
        for column, rows in report["date_violations"].items():
            print(f"\nColumn: {column}")
            print(f"Invalid Rows: {len(rows)}")
            print_rows(rows)
        print()
    else:
        print("Date Validation Violations: None\n")

    if report["string_violations"]:
        print("String Validation Violations:")
        for column, rows in report["string_violations"].items():
            print(f"\nColumn: {column}")
            print(f"Invalid Rows: {len(rows)}")
            print_rows(rows)
        print()
    else:
        print("String Validation Violations: None\n")

    if not report["duplicate_key_violations"].empty:
        print("Duplicate Uniqueness Key Violations:")
        print(f"Uniqueness Key: {', '.join(UNIQUENESS_KEYS)}")
        print(f"Invalid Rows: {len(report['duplicate_key_violations'])}")
        print_rows(report["duplicate_key_violations"])
        print()
    else:
        print("Duplicate Uniqueness Key Violations: None\n")

    has_errors = (
        len(report["missing_columns"]) > 0
        or len(report["unexpected_columns"]) > 0
        or len(report["null_violations"]) > 0
        or len(report["integer_violations"]) > 0
        or len(report["date_violations"]) > 0
        or len(report["string_violations"]) > 0
        or not report["duplicate_key_violations"].empty
    )

    if has_errors:
        print("Validation Result: ❌ FAILED")
    else:
        print("Validation Result: ✅ PASSED")


# =============================
# EXCEL FILE PATH GOES HERE
# =============================

file_path = (
    r"C:\C:\Users\<USER>\<COMPANY>\<PARENT>"
    r"\Power BI Source Files\Grant Enrollments\GrantEnrollments_ServicesProvided.xlsx"
)


# =============================
# READ EXCEL
# =============================

df = pd.read_excel(
    file_path,
    dtype="string"
)


# =============================
# RUN VALIDATION
# =============================

report = validate_excel(df)

print_report(report)

