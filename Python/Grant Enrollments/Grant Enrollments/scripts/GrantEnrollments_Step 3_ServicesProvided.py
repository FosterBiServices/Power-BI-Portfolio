# # Grant Enrollments SERVICES PROVIDED 
# ## Step 3: Transform and Prepare Services Provided Data
# 
# ## Purpose
# 
# This step extracts, validates, cleans, and standardizes AJCC service activity records from the source workbook.
# 
# The source file contains report formatting, repeated headers, summary rows, and inconsistent text formatting that must be normalized before the data can be used for validation and Power BI reporting.
# 
# The resulting dataset becomes the authoritative service activity source used throughout the downstream validation and reporting process.
# 
# ## Source File
# 
# The process automatically searches for a source workbook containing the text GrantEnrollments_ServicesProvided.
# 
# ## Source Directory
# **Users\<USER>\Downloads\Grant Enrollments\Files for Python**
# ### File Validation Rules
# - Exactly one matching file must exist.
# - Processing fails if no matching file is found.
# - Processing fails if multiple matching files are found.
# 
# These safeguards prevent accidental processing of outdated, duplicate, or incorrect source files.
# 
# ## Region Mapping
# 
# A hardcoded lookup table is used to map each Workforce Development Board to its associated Region Code.
# 
# The Region Code is appended to the final output dataset and is used for:
# 
# - Regional reporting
# - Data model relationships
# - Validation activities
# - Power BI filtering and aggregation
# 
# ## Data Preparation Process
#   
# ### Header Detection
# - Load the source worksheet without predefined headers.
# - Locate the row containing the User ID field.
# - Promote the identified row to the dataset header.
# 
# ## Column Standardization
# 
# The process performs the following cleanup activities:
# 
# - Remove rows above the identified header row.
# - Remove repeated header rows contained within the dataset.
# - Remove summary and total rows.
# - Remove blank records caused by Excel used-range issues.
# - Standardize column names.
# - Rename Region/LWDB to REGION LWDB.
# - Convert all column names to uppercase.
# 
# ## Data Type Validation
# 
# Before processing continues, the dataset is validated against expected data types.
# 
# ## String Fields
# 
# The following fields must contain valid text values:
# 
# - REGION LWDB
# - Office
# - Office of Responsibility
# - Service
# - NAICS
# - ONET
# - Completion Status
# - Program
# - Provider
# - Registered Apprenticeship
# - Type of Apprenticeship
# - Hispanic
# - Learning Mode
# - Agency Code
# - Ex Offender
# - Comments
# 
# ### Numeric Fields
# 
# The following fields must contain valid numeric values:
# 
# - User ID
# - State ID
# - App ID
# - 
# ### Date Fields
# 
# The following fields must contain valid dates when populated:
# 
# - Create Date
# - Actual Begin Date
# - Projected Begin Date
# - Actual End Date
# - Projected End Date
# - Most Recent Employment Date
# 
# Processing stops immediately if any expected field is missing or contains invalid data types.
# 
# ## Data Standardization
# 
# To improve reporting consistency, text fields are standardized before aggregation.
# 
# ## Text Cleanup
# - Leading and trailing spaces are removed.
# - Text formatting inconsistencies are corrected.
# - Duplicate values caused by inconsistent capitalization are reduced.
# - Proper Case Standardization
# 
# The following fields are converted to Proper Case:
# 
# - Office
# - Office of Responsibility
# - Service
# - NAICS
# - ONET
# - Completion Status
# - Program
# - Provider
# - Registered Apprenticeship
# - Type of Apprenticeship
# - Hispanic
# - Learning Mode
# - Agency Code
# - Ex Offender
# - Comments
# - Upper Case Standardization
# 
# The following fields are converted to uppercase:
# 
# - Agency Code
# - Service Consolidation Logic
# 
# Service records are grouped using all reporting attributes contained within the dataset.
# 
# ## The process:
# 
# - Consolidates duplicate service records.
# - Preserves blank date values during grouping.
# - Counts occurrences using USER ID.
# - Produces a single summarized record for each unique service combination.
# 
# This approach reduces duplicate reporting records while preserving service activity metrics.
# 
# ## Region Code Assignment
# 
# After aggregation is complete, the process assigns a Region Code using the predefined Workforce Development Board lookup table.
# 
# This ensures all output records contain both:
# 
# 1. REGION LWDB
# 2. REGION CODE
# 
# These fields support downstream reporting and model relationships.
# 
# ## Output File
# ## Output Directory
# **Users\<USER>\Downloads\Grant Enrollments**
# Output File Name
# **GrantEnrollments_ServicesProvided.xlsx**
# 
# If the file already exists, it is automatically overwritten.
# 
# ## Expected Outcome
# 
# The generated file should contain:
# 
# - Standardized column names
# - Validated data types
# - Consistent text formatting
# - No repeated header rows
# - No summary rows
# - No blank records
# - Consolidated service activity records
# - Assigned Region Codes
# 
# The resulting dataset becomes the source for downstream validation activities and Power BI refresh processing.
# 
# ## Failure Conditions
# 
# Processing stops when:
# 
# - No matching source workbook is found.
# - Multiple matching source workbooks are found.
# - The User ID header row cannot be located.
# - Required columns are missing.
# - Invalid numeric values are encountered.
# - Invalid date values are encountered.
# - Invalid text values are encountered.
# 
# These controls help ensure that only clean, validated, and report-ready data enters the reporting workflow.
# 
# 

# In[ ]:





# In[11]:


import pandas as pd
from pathlib import Path

# User home directory (dynamic)
home_dir = Path.home()

# SharePoint relative path inside OneDrive
sharepoint_relative_input_path = Path(
    "<COMPANY>",
    "<SITE>",
    "<PARENT>",
    "<CHILD>",
    "<CHILD2>"
)


source_dir = home_dir / sharepoint_relative_input_path

# # 🔥 File for conversion
file_substring = "GrantEnrollments_ServicesProvided"

# 🧐 Get files matching substring
matching_files = [
    f for f in source_dir.glob("*.xlsx")
    if file_substring in f.name
]
# ☠️ No files matching error message
if not matching_files:
    raise FileNotFoundError("No matching Excel file found.")

# ☠️ Muiltiple files matching substring error message
if len(matching_files) > 1:
    raise ValueError(
        f"Multiple matching files found:\n{[f.name for f in matching_files]}"
    )

input_path = matching_files[0]

print(f"✅ Using file: {input_path}")

sharepoint_relative_output_path = Path(
    "<COMPANY>",
    "<SITE>",
    "<PARENT>",
    "<CHILD>",
    "<CHILD2>"
)


target_dir = home_dir / sharepoint_relative_output_path

# 📁 Full path with name for output file 
output_path = rf'{target_dir}\{file_substring}.xlsx'
# ## Validation of locations ## # print(f'Input: {input_path}\n\nOutput: {output_path}')

REGION_CODE_LOOKUP = {
    "Alameda Workforce Board": 1,
    "Prairie Glen Workforce Board": 7,
    "Amberfield Workforce Board": 8,
    "Lakebridge Workforce Board": 12,
    "Maple Crossing Workforce Board": 15,
    "Rivermoor Workforce Board": 20,
    "Pine Hollow Workforce Board": 22,
    "Oakmere Workforce Board": 23,
    "Clearfork Workforce Board": 28,
    "Grand Meadow Workforce Board": 29,
    "Silver Creek Workforce Board": 32,
    "Redstone Workforce Board": 33,
    "Elm Harbor Workforce Board": 35,
    "Stonefield Workforce Board": 43,
    "Briar Lake Workforce Board": 45,
    "Westhaven Workforce Board": 48,
    "Meadowbrook Workforce Board": 50
}
# 🛻 Load the 1st worksheet with NO headers
df_raw = pd.read_excel(input_path, sheet_name=0, header=None)

# 🛻 Find the row index where column 0 == "User ID"
header_row_idx = df_raw.index[df_raw.iloc[:, 0] == "User ID"]

# ☠️ Error message when column header not located
if header_row_idx.empty:
    raise ValueError("Header row containing 'User ID' not found.")

header_row_idx = header_row_idx[0]

# ➖ Remove rows above the header
df_clean = df_raw.iloc[header_row_idx:].reset_index(drop=True)

# 🛻 Promote that row to headers
df_clean.columns = df_clean.iloc[0]
df_clean = df_clean.iloc[1:].reset_index(drop=True)

# ✔️ Clean column names
df_clean.columns = (
    df_clean.columns
        .astype(str)
        .str.replace('\n', ' ', regex=False)  # replace newline with space
        .str.replace(r'\s+', ' ', regex=True) # collapse multiple spaces
        .str.strip()                           # trim leading/trailing spaces
)

# 🔄 Rename column header with # to Code
if "Region/LWDB" in df_clean.columns:
    print("ℹ️ Renaming 'Region/LWDB' → 'REGION LWDB'")

    # Rename column
    df_clean = df_clean.rename(columns={"Region/LWDB": "REGION LWDB"})


# ➖ Remove repeated header rows inside the data
df_clean = df_clean[df_clean["User ID"] != "User ID"]

# ➖ Remove total row
df_clean = df_clean[~df_clean["User ID"].astype(str).str.contains(
    "Total", na=False
)]

# 4️⃣ Validate columns are present 
expected_string_cols = ["REGION LWDB","Office","Office of Responsibility","Service","NAICS","ONET","Completion Status","Program","Provider","Registered Apprenticeship","Type of Apprenticeship","Hispanic","Learning Mode","Agency Code","Ex Offender","Comments"] #"Staff Edited"
expected_numeric_cols = ["User ID", "State ID", "App ID"]
expected_date_cols = ["Create Date","Actual Begin Date","Projected Begin Date",	"Actual End Date","Projected End Date","Most recent Employment Date"]

for col in expected_string_cols:
    if col not in df_clean.columns:
        raise ValueError(f"❌ Missing expected string column: '{col}'")

    # Convert to string
    df_clean[col] = df_clean[col].astype("string")

    # Verify all values are strings (or NA)
    bad_mask = df_clean[col].apply(lambda v: not (pd.isna(v) or isinstance(v, str)))
    if bad_mask.any():
        bad_values = df_clean.loc[bad_mask, col].head(10)
        raise TypeError(
            f"❌ Column '{col}' contains non-string data.\n"
            f"Example invalid values:\n{bad_values}"
        )

for col in expected_numeric_cols:
    if col not in df_clean.columns:
        raise ValueError(f"❌ Missing expected numeric column: '{col}'")

    # Try converting to numeric
    converted = pd.to_numeric(df_clean[col], errors="coerce")

    # If any value becomes NaN but original was not NaN → bad data
    bad_mask = converted.isna() & df_clean[col].notna()
    if bad_mask.any():
        bad_values = df_clean.loc[bad_mask, col].head(10)
        raise TypeError(
            f"❌ Column '{col}' contains non-numeric data.\n"
            f"Example invalid values:\n{bad_values}"
        )

    # Assign validated numeric version
    df_clean[col] = converted


for col in expected_date_cols:
    if col not in df_clean.columns:
        raise ValueError(f"❌ Missing expected date column: '{col}'")

    converted = pd.to_datetime(df_clean[col], errors="coerce")

    # invalid dates = rows that became NaT but were not originally empty
    bad_mask = converted.isna() & df_clean[col].notna() & (df_clean[col].astype(str).str.strip() != "")
    if bad_mask.any():
        bad_values = df_clean.loc[bad_mask, col].head(10)
        raise TypeError(
            f"❌ Column '{col}' contains invalid date values.\n"
            f"Example invalid values:\n{bad_values}"
        )

    df_clean[col] = converted

print("✅ All column types validated successfully. Safe to continue.")

# 🤖 Capitlize headers
df_clean.columns = df_clean.columns.str.upper()

# 🤖 Drop blank rows, fail back for "used range" in excel file
df_clean = df_clean.dropna(how="all")

# 🤖 Trim all text columns with diagnostics
text_cols = df_clean.select_dtypes(include=["object", "string"]).columns

for col in text_cols:
    #print(f"Processing {col} ({df_clean[col].dtype})")

    try:
        df_clean[col] = df_clean[col].astype("string").str.strip()
    except Exception as e:
        print(f"ERROR IN COLUMN: {col}")
        print(f"DTYPE: {df_clean[col].dtype}")
        # print(df_clean[col].head())
        raise

# 😎 Clean up case miss matches before aggregating data 
proper_case_cols = [
    "Office",
    "Office of Responsibility",
    "Service",
    "NAICS",
    "ONET",
    "Completion Status",
    "Program",
    "Provider",
    # "Staff Edited",
    "Registered Apprenticeship",
    "Type of Apprenticeship",
    "Hispanic",
    "Learning Mode",
    "Agency Code",
    "Ex Offender",
    "Comments"
]
upper_case_cols = [
    "Agency Code"        
]
# Proper Case columns
for col in proper_case_cols:
    if col in df_clean.columns:
        df_clean[col] = (
            df_clean[col]
            .astype("string")
            .str.strip()
            .str.title()
        )
#Upper case columns
for col in upper_case_cols:
    if col in df_clean.columns:
        df_clean[col] = (
            df_clean[col]
            .astype("string")
            .str.strip()
            .str.upper()
        )

df_extended = df_clean.copy()

# ➕ Limit to only fields needed
df_clean_agg = (
    df_extended
    .groupby(
        [
        "REGION LWDB",
        "OFFICE",
        "OFFICE OF RESPONSIBILITY",
        "SERVICE",
        "NAICS",
        "ONET",
        "COMPLETION STATUS",
        "PROGRAM",
        "PROVIDER",
        # "STAFF EDITED",
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
    ],
        as_index=False,
        dropna=False   # 🔥 Needs to remain here because of grouping, dates may be blank which would be removed
    )["USER ID"]
    .count()
)

# 🤖 Trim all text columns
text_cols = df_clean_agg.select_dtypes(include=["object", "string"]).columns

df_clean_agg[text_cols] = df_clean_agg[text_cols].apply(
    lambda col: col.str.strip()
)

# ➕ Map REGION CODE
df_clean_agg["REGION CODE"] = df_clean_agg["REGION LWDB"].map(REGION_CODE_LOOKUP)


# 🤖 Convert output path to pathlib path 
output_path = Path(output_path)

# 🤖 Check if file exists and remove 
if output_path.exists():
    print(f"⚠️ Overwriting existing file: {output_path}")
    output_path.unlink()  # deletes the file
else: 
    print(f"🆕 File does not exist. Creating new file at: {output_path}")

# ✍️ Export to Excel
df_clean_agg.to_excel(output_path, index=False)

