
# ## Funder Budget Validation and Transformation
# 
# This process prepares the <COMPANY> funder budget file for reporting and financial analysis by validating required fields, enforcing data quality rules, and standardizing project codes prior to export.
# 
# Key steps performed:
# 
# - Loads the <COMPANY> funder budget workbook.
# - Standardizes the first column name when the source file contains an unnamed or inconsistent header.
# - Validates the presence of all required columns.
# - Verifies expected data types for:
#   - Name
#   - Code
#   - Account Description
#   - Account
#   - Amount
#   - Company
#   - Fiscal Year
#   - Date From
#   - Date To
# - Replaces blank



import pandas as pd

input_excel_path = r'C:\Users\<USER>\Downloads\<COMPANY> Funder Budgets FY26.xlsx'
output_csv_path = r'C:\Users\<USER>\Downloads\<COMPANY> Funder Budgets FY26.csv'       
sheet_name = None                    
code_column = "Code"               

df = pd.read_excel(input_excel_path)

first_col = df.columns[0]

if (
    first_col is None
    or (isinstance(first_col, str) and first_col.lower().startswith("unnamed"))
    or (isinstance(first_col, str) and first_col.strip().lower() == "center")
):
    df = df.rename(columns={first_col: "Name"})
    print(f"Renamed first column '{first_col}' → 'Name'")
else:
    print(f"First column already named: {first_col}")


expected_string_cols = ["Name", "Code", "Account Description"]
expected_numeric_cols = ["Account", "Amount", "Company", "Fiscal Year"]
expected_date_cols = ["Date From", "Date To"]

df['Amount'] = df['Amount'].fillna(0)

for col in expected_string_cols:
    if col not in df.columns:
        raise ValueError(f"❌ Missing expected string column: '{col}'")

    # Convert to string
    df[col] = df[col].astype("string")

    # Verify all values are strings (or NA)
    bad_mask = df[col].apply(lambda v: not (pd.isna(v) or isinstance(v, str)))
    if bad_mask.any():
        bad_values = df.loc[bad_mask, col].head(10)
        raise TypeError(
            f"❌ Column '{col}' contains non-string data.\n"
            f"Example invalid values:\n{bad_values}"
        )

for col in expected_numeric_cols:
    if col not in df.columns:
        raise ValueError(f"❌ Missing expected numeric column: '{col}'")

    # Try converting to numeric
    converted = pd.to_numeric(df[col], errors="coerce")

    # If any value becomes NaN but original was not NaN → bad data
    bad_mask = converted.isna() & df[col].notna()
    if bad_mask.any():
        bad_values = df.loc[bad_mask, col].head(10)
        raise TypeError(
            f"❌ Column '{col}' contains non-numeric data.\n"
            f"Example invalid values:\n{bad_values}"
        )

    # Assign validated numeric version
    df[col] = converted


for col in expected_date_cols:
    if col not in df.columns:
        raise ValueError(f"❌ Missing expected date column: '{col}'")

    converted = pd.to_datetime(df[col], errors="coerce")

    # invalid dates = rows that became NaT but were not originally empty
    bad_mask = converted.isna() & df[col].notna() & (df[col].astype(str).str.strip() != "")
    if bad_mask.any():
        bad_values = df.loc[bad_mask, col].head(10)
        raise TypeError(
            f"❌ Column '{col}' contains invalid date values.\n"
            f"Example invalid values:\n{bad_values}"
        )

    df[col] = converted

    if "Date From" in df.columns and "Date To" in df.columns:
        # Only compare where both dates are present
        compare_mask = df["Date From"].notna() & df["Date To"].notna()
        violation_mask = compare_mask & (df["Date From"] > df["Date To"])
        if violation_mask.any():
            bad_rows = df.index[violation_mask].tolist()[:10]
            bad_sample = df.loc[violation_mask, ["Date From", "Date To"]].head(10)
            raise ValueError(
                "❌ Date rule violation: 'Date From' cannot be after 'Date To'.\n"
                f"Example invalid rows: {bad_rows}\n"
                f"Sample:\n{bad_sample}"
            )


print("✅ All column types validated successfully. Safe to continue.")

df["CPROJ_TASK"] = df["Code"]

if code_column not in df.columns:
    raise KeyError(f"Column '{CODE_COLUMN}' not found. Available columns: {list(df.columns)}")

col = df[code_column].astype("string")

df[code_column] = col.str.split("-", n=3).str[:3].str.join("-")

df.to_csv(output_csv_path, index=False, encoding="utf-8")

print(f"CSV saved")



# In[5]:


import pandas as pd

input_excel_path = r'C:\Users\<USER>\Downloads\<COMPANY> Funder Budgets FY26.xlsx'
output_csv_path = r'C:\Users\<USER>\Downloads\<COMPANY> Funder Budgets FY26.csv'       
sheet_name = None                    
code_column = "Code"               

df = pd.read_excel(input_excel_path)

first_col = df.columns[0]

if (
    first_col is None
    or (isinstance(first_col, str) and first_col.lower().startswith("unnamed"))
    or (isinstance(first_col, str) and first_col.strip().lower() == "center")
):
    df = df.rename(columns={first_col: "Name"})
    print(f"Renamed first column '{first_col}' → 'Name'")
else:
    print(f"First column already named: {first_col}")

expected_string_cols = ["Name", "Code", "Account Description"]
expected_numeric_cols = ["Account", "Amount", "Company", "Fiscal Year"]
expected_date_cols = ["Date From", "Date To"]

df['Amount'] = df['Amount'].fillna(0)

for col in expected_string_cols:
    if col not in df.columns:
        raise ValueError(f"❌ Missing expected string column: '{col}'")

    # Convert to string
    df[col] = df[col].astype("string")

    # Verify all values are strings (or NA)
    bad_mask = df[col].apply(lambda v: not (pd.isna(v) or isinstance(v, str)))
    if bad_mask.any():
        bad_values = df.loc[bad_mask, col].head(10)
        raise TypeError(
            f"❌ Column '{col}' contains non-string data.\n"
            f"Example invalid values:\n{bad_values}"
        )

for col in expected_numeric_cols:
    if col not in df.columns:
        raise ValueError(f"❌ Missing expected numeric column: '{col}'")

    # Try converting to numeric
    converted = pd.to_numeric(df[col], errors="coerce")

    # If any value becomes NaN but original was not NaN → bad data
    bad_mask = converted.isna() & df[col].notna()
    if bad_mask.any():
        bad_values = df.loc[bad_mask, col].head(10)
        raise TypeError(
            f"❌ Column '{col}' contains non-numeric data.\n"
            f"Example invalid values:\n{bad_values}"
        )

    # Assign validated numeric version
    df[col] = converted


for col in expected_date_cols:
    if col not in df.columns:
        raise ValueError(f"❌ Missing expected date column: '{col}'")

    converted = pd.to_datetime(df[col], errors="coerce")

    # invalid dates = rows that became NaT but were not originally empty
    bad_mask = converted.isna() & df[col].notna() & (df[col].astype(str).str.strip() != "")
    if bad_mask.any():
        bad_values = df.loc[bad_mask, col].head(10)
        raise TypeError(
            f"❌ Column '{col}' contains invalid date values.\n"
            f"Example invalid values:\n{bad_values}"
        )

    df[col] = converted

    if "Date From" in df.columns and "Date To" in df.columns:
        # Only compare where both dates are present
        compare_mask = df["Date From"].notna() & df["Date To"].notna()
        violation_mask = compare_mask & (df["Date From"] > df["Date To"])
        if violation_mask.any():
            bad_rows = df.index[violation_mask].tolist()[:10]
            bad_sample = df.loc[violation_mask, ["Date From", "Date To"]].head(10)
            raise ValueError(
                "❌ Date rule violation: 'Date From' cannot be after 'Date To'.\n"
                f"Example invalid rows: {bad_rows}\n"
                f"Sample:\n{bad_sample}"
            )


print("✅ All column types validated successfully. Safe to continue.")

df["CPROJ_TASK"] = ""

if code_column not in df.columns:
    raise KeyError(f"Column '{CODE_COLUMN}' not found. Available columns: {list(df.columns)}")

col = df[code_column].astype("string")

df[code_column] = col.str.split("-", n=3).str[:3].str.join("-")

df.to_csv(output_csv_path, index=False, encoding="utf-8")

print(f"CSV saved")



# In[ ]:




