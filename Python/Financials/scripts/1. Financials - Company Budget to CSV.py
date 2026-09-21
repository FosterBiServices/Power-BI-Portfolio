# ## Budget File Validation and CSV Conversion
# 
# This process prepares the FY2027 budget workbook for downstream reporting and data integration by validating key fields and converting the source Excel file to CSV format.
# 
# Key steps performed:
# 
# - Loads the budget workbook from the designated file location.
# - Standardizes budget amount column names when alternate naming conventions are detected.
# - Removes currency formatting from budget amount values.
# - Validates the presence of all required columns.
# - Verifies expected data types for:
#   - General Ledger Account Code
#   - Profit Center Code
#   - Budget Balance Amount
#   - Company
#   - Fiscal Date

# In[ ]:





# In[3]:


import pandas as pd

input_excel_path = r'C:\Users\<USER>\Downloads\<COMPANY> Budget - FY2027.xlsx'
output_csv_path = r'C:\Users\<USER>\Downloads\<COMPANY> Budget - FY2027.csv'       


df = pd.read_excel(input_excel_path)

expected_string_cols = ["GL Account Code", "Profit Center Code"]
expected_numeric_cols = ["Budget Balance Amount", "Company"]
expected_date_cols = ["Fiscal Date"]

# --- Normalize Budget Amount column if present ---

if "Budget Amount" in df.columns:
    print("ℹ️ Renaming 'Budget Amount' → 'Budget Balance Amount'")

    # Rename column
    df = df.rename(columns={"Budget Amount": "Budget Balance Amount"})

    # Strip currency symbols and commas, then convert to numeric
    df["Budget Balance Amount"] = (
        df["Budget Balance Amount"]
            .astype(str)
            .str.replace(r"[\$,]", "", regex=True)
            .str.strip()
    )

if "GL Account" in df.columns:
    print("ℹ️ Renaming 'GL Account' → 'GL Account Code'")

    # Rename column
    df = df.rename(columns={"GL Account": "GL Account Code"})

if "Profit Center" in df.columns:
    print("ℹ️ Renaming 'Profit Center' → 'Profit Center Code'")

    # Rename column
    df = df.rename(columns={"Profit Center": "Profit Center Code"})


# Ensure column exists (either originally or renamed)
if "Budget Balance Amount" not in df.columns:
    raise ValueError("❌ Missing required column: 'Budget Balance Amount'")

df['Budget Balance Amount'] = df['Budget Balance Amount'].fillna(0)

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

print("✅ All column types validated successfully. Safe to continue.")

df.to_csv(output_csv_path, index=False, encoding="utf-8")

print(f"CSV saved")



# In[1]:


import pandas as pd

input_excel_path = r'C:\Users\<USER>\Downloads\<COMPANY> Budget - FY2027.xlsx'
output_csv_path = r'C:\Users\<USER>\Downloads\<COMPANY> Budget - FY2027.csv'       


df = pd.read_excel(input_excel_path)

expected_string_cols = ["GL Account Code", "Profit Center Code"]
expected_numeric_cols = ["Budget Balance Amount", "Company"]
expected_date_cols = ["Fiscal Date"]

# --- Normalize Budget Amount column if present ---

if "Company Code" in df.columns:
    print("ℹ️ Renaming 'Company Code' → 'Company'")

    # Rename column
    df = df.rename(columns={"Company Code": "Company"})

if "Budget Amount" in df.columns:
    print("ℹ️ Renaming 'Budget Amount' → 'Budget Balance Amount'")

    # Rename column
    df = df.rename(columns={"Budget Amount": "Budget Balance Amount"})

if "Value" in df.columns:
    print("ℹ️ Renaming 'Value' → 'Budget Balance Amount'")

    # Rename column
    df = df.rename(columns={"Value": "Budget Balance Amount"})

    # Strip currency symbols and commas, then convert to numeric
    df["Budget Balance Amount"] = (
        df["Budget Balance Amount"]
            .astype(str)
            .str.replace(r"[\$,]", "", regex=True)
            .str.strip()
    )

# Ensure column exists (either originally or renamed)
if "Budget Balance Amount" not in df.columns:
    raise ValueError("❌ Missing required column: 'Budget Balance Amount'")

df['Budget Balance Amount'] = df['Budget Balance Amount'].fillna(0)

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

print("✅ All column types validated successfully. Safe to continue.")

df.to_csv(output_csv_path, index=False, encoding="utf-8")

print(f"CSV saved")



# In[2]:


import pandas as pd

input_excel_path = r'C:\Users\<USER>\Downloads\<COMPANY> Budget - FY2027.xlsx'
output_csv_path = r'C:\Users\<USER>\Downloads\<COMPANY> Budget - FY2027.csv'       


df = pd.read_excel(input_excel_path)

expected_string_cols = ["GL Account Code", "Profit Center Code"]
expected_numeric_cols = ["Budget Balance Amount", "Company"]
expected_date_cols = ["Fiscal Date"]

# --- Normalize Budget Amount column if present ---

if "Company Code" in df.columns:
    print("ℹ️ Renaming 'Company Code' → 'Company'")

    # Rename column
    df = df.rename(columns={"Company Code": "Company"})

if "Budget Amount" in df.columns:
    print("ℹ️ Renaming 'Budget Amount' → 'Budget Balance Amount'")

    # Rename column
    df = df.rename(columns={"Budget Amount": "Budget Balance Amount"})

if "Value" in df.columns:
    print("ℹ️ Renaming 'Value' → 'Budget Balance Amount'")

    # Rename column
    df = df.rename(columns={"Value": "Budget Balance Amount"})

    # Strip currency symbols and commas, then convert to numeric
    df["Budget Balance Amount"] = (
        df["Budget Balance Amount"]
            .astype(str)
            .str.replace(r"[\$,]", "", regex=True)
            .str.strip()
    )

# Ensure column exists (either originally or renamed)
if "Budget Balance Amount" not in df.columns:
    raise ValueError("❌ Missing required column: 'Budget Balance Amount'")

df['Budget Balance Amount'] = df['Budget Balance Amount'].fillna(0)

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

print("✅ All column types validated successfully. Safe to continue.")

df.to_csv(output_csv_path, index=False, encoding="utf-8")

print(f"CSV saved")


