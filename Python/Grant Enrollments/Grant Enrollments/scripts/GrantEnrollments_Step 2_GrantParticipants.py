# # Grant Enrollments PARTICIPANTS
# ## Step 2: Transform and Prepare Grant Participant Data
# 
# ### Purpose
# 
# This step extracts, cleans, and standardizes participant-level grant activity data from the source AJCC workbook.
# The source file contains report formatting, non-data rows, repeated headers, and summary records that must be removed before the data can be used for validation and reporting.
# The resulting dataset is structured for downstream quality checks and Power BI consumption.
# 
# ### Source Directory
# **Users\<USER>\Downloads\Grant Enrollments\Files for Python**
#     
# ### File Selection Rules
# - Exactly one file containing GrantEnrollments_GrantParticipants must exist.
# - If no matching file is found, the process fails.
# - If multiple matching files are found, the process fails.
# 
# These controls prevent accidental processing of outdated or duplicate source files.
# 
# ### Data Preparation Process
# 
# The following transformation steps are performed:
# 
# ### File Discovery
# - Locate the Grant Participants workbook.
# - Validate that exactly one matching file exists.
# - Header Identification
# - Load the worksheet without predefined headers.
# - Locate the row containing the "Grant" column header.
# - Promote the identified row to the dataset header.
# ### Data Cleanup
# - Remove rows above the actual header row.
# - Remove repeated header rows appearing within the dataset.
# - Remove summary and total rows.
# - Standardize column names.
# - Remove blank rows caused by Excel used-range issues.
# - Convert all column names to uppercase.
#     
# ## Data Type Standardization
# 
# The following field is converted to a numeric data type:
# 
# - LWDB
# 
# An error is raised if invalid numeric values are encountered.
# 
# ## Included Fields
# 
# Only fields required for reporting and validation are retained.
# 
# - Participant Fields
# - LWDB
# - APP ID
# - RESPONSIBLE OFFICE
# - PARTICIPATION DATE
# - GRANT ENROLL DATE
# - LAST GRANT ACTIVITY DATE
# - PROJECTED GRANT ACTIVITY END DATE
# - EXIT DATE
# - RECEIVED CREDENTIAL
# - ENTERED EMPLOYMENT
# - WITH DISABILITY
# 
# All other source report columns are excluded from the final output.
# 
# ## Aggregation Logic
# 
# Participant records are grouped by the reporting attributes listed above.
# 
# ### The process then:
# 
# - Counts the number of participant records (APP ID) within each unique grouping.
# - Preserves blank date values during grouping.
# - Removes groupings with zero participant counts.
# 
# This step creates a clean participant dataset suitable for validation and reporting.
# 
# ## Output Directory
# **Users\<USER>\Downloads\Grant Enrollments**
# - Output File Name
#   - GrantEnrollments_GrantParticipants.xlsx
# 
# If a file already exists, it is automatically replaced with the newly generated version.
# 
# ## Expected Outcome
# 
# The output file should contain:
# 
# - Standardized column names
# - Clean participant records
# - No report header rows
# - No summary rows
# - No blank records
# - Aggregated participant counts
# 
# The resulting file becomes the source for downstream validation and Power BI refresh activities.
# 
# ## Failure Conditions
# 
# The process will stop execution when:
# 
# - No matching source file is found.
# - Multiple matching source files are found.
# - The `Grant` header row cannot be located.
# - Invalid numeric values are encountered in the LWDB field.
# 
# These safeguards help ensure that only valid and expected source data enters the reporting workflow.

# In[ ]:





# In[1]:


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
file_substring = "GrantEnrollments_GrantParticipants"

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

# 🛻 Load the 4th worksheet with NO headers
df_raw = pd.read_excel(input_path, sheet_name=0, header=None)

# 🛻 Find the row index where column 0 == "Grant"
header_row_idx = df_raw.index[df_raw.iloc[:, 1] == "Grant"]

# ☠️ Error message when column header not located
if header_row_idx.empty:
    raise ValueError("Header row containing 'Grant' not found.")

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

# ➖ Remove repeated header rows inside the data
df_clean = df_clean[df_clean["Grant"] != "Grant"]

# ➖ Remove total row
df_clean = df_clean[~df_clean["Grant"].astype(str).str.contains(
    "Total", na=False
)]

# 🤖 Capitlize headers
df_clean.columns = df_clean.columns.str.upper()

# 🤖 Drop blank rows, fail back for "used range" in excel file
df_clean = df_clean.dropna(how="all")


# ➕ Convert LWDB to numeric (nullable integer)
df_clean["LWDB"] = (
    pd.to_numeric(df_clean["LWDB"], errors="raise")
      .astype("Int64")
)

# ➕ Limit to only fields needed
cols_to_keep = [
    # "GRANT", 
    "LWDB",
    # "STATE ID",
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
    # , "CAREER SERVICES", 
    # "EDU / TRAIN", 
    # "OJT", 
    # "WORK EXP.", 
    # "SUPPORT SERVICES", 
    # "DWG DISASTER ONLY", 
    # "CO-ENROLLED", 
    # "WP", 
    # "AD", 
    # "DW", 
    # "RR ADD. ASSIST", 
    # "YOUTH", 
    # "DWG", 
    # "IWT", 
    # "NON-WIOA GRANT", 
    # "LOCAL GRANT", 
    # "TAA", 
    # "NFJP", 
    # "OTHER", 
    # "HISPANIC", 
    # "AMER. INDIAN / ALASKAN NATIVE", 
    # "ASIAN", 
    # "AFRICIAN AMERICAN/ BLACK", 
    # "NATIVE HAWAIIAN", 
    # "WHITE", 
    # "MULTI-RACIAL", 
    # "ELIG. VET", 
    # "WITH DISABILITY", 
    # "UNEMPLOYED", 
    # "UNDEREMPLOYED", 
    # "DISLOCATED WORKER", 
    # "INCUMBENT WORKER", 
    # "NO SCHOOL LEVEL", 
    # "SEC SCHOOL GRAD", 
    # "1 + YRS OFPS EDU", 
    # "PS EDU CERT", 
    # "AS/AA DEGREE", 
    # "BS/BA DEGREE", 
    # "BEYOND BA/BS DEGREE", 
    # "DISPLAYED HOMEMAKER", 
    # "LOW INCOME", 
    # "OLDER IND", 
    # "EX OFFENDER", 
    # "HOMELESS / RUNAWAY", 
    # "FOSTER CARE YTH", 
    # "BSD / ENGLISH LEARN", 
    # "EXHAST. TANF", 
    # "SINGLE PARENT", 
    # "LONG TERM UNEMPL."
]

df_raw = df_clean[cols_to_keep].copy()

# 📊 Aggregate fields

df_clean_agg = (
    df_raw
    .groupby(
        [
            "LWDB",
            # "STATE ID",
            "RESPONSIBLE OFFICE",
            "PARTICIPATION DATE",
            "GRANT ENROLL DATE",
            "LAST GRANT ACTIVITY DATE",
            "PROJECTED GRANT ACTIVITY END DATE",
            "EXIT DATE",
            "RECEIVED CREDENTIAL",
            "ENTERED EMPLOYMENT",
            "WITH DISABILITY"
        ],
        as_index=False,
        dropna=False   # 🔥 Needs to remain here because of grouping, dates may be blank which would be removed
    )["APP ID"]
    .count()
)

# 🤖 Drop blank rows, with a 0 for user name count ( grouping of all columns but no users )
df_clean_agg = df_clean_agg[df_clean_agg["APP ID"] > 0]

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

