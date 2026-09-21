#!/usr/bin/env python
# coding: utf-8

# ## Legacy Hierarchy Transformation
# 
# This process converts the Legacy Hierarchy workbook into a standardized reporting hierarchy that supports historical and current organizational mappings.
# 
# Key steps performed:
# 
# - Loads the Master Data worksheet from the hierarchy workbook.
# - Dynamically locates the hierarchy starting point using the `Location` field.
# - Removes introductory rows and columns that are not part of the hierarchy data.
# - Promotes the identified header row.
# - Cleans whitespace from all text fields.
# - Filters records that contain legacy mappings.
# - Splits multiple legacy codes into individual values.
# - Expands legacy mappings into separate records.
# - Reassigns legacy codes as the primary Cost Center / Profit Center values.
# - Aligns profit center names to the reporting roll-up structure.
# - Rebuilds reporting hierarchy fields using current organizational mappings.
# - Selects only reporting-relevant hierarchy columns.
# - Removes duplicate records.
# - Exports the final hierarchy to CSV format.
# 
# ### Hierarchy Transformations
# 
# The process performs several business-rule transformations:
# 
# - Expands multiple legacy codes stored in a single field into separate rows.
# - Maps each legacy code to its associated reporting hierarchy.
# - Replaces profit center values with legacy identifiers where applicable.
# - Aligns location values with Cost Center / Profit Center reporting structures.
# - Preserves roll-up relationships for:
#   - Company
#   - Line of Business
#   - Product Category
#   - Segment
#   - Cost Center / Profit Center
# 
# ### Output
# 
# **Source File:** `Legacy Hierarchy.xlsx`
# 
# **Output File:** `Legacy Hierarchy.csv`
# 
# **Result:** A flattened hierarchy lookup table containing legacy organizational mappings and current reporting relationships for use in reporting, data integration, and historical trend analysis.

# In[ ]:





# In[5]:


import pandas as pd
# Load Excel file
file_path = r'C:\Users\<USER>\Downloads\Legacy Hierarchy.xlsx'
xls = pd.ExcelFile(file_path, engine='openpyxl')
df = xls.parse('Master Data', header=None)
xls.close()  # <-- Close the file handle

# Find the first cell that contains 'Location'
location_row_index = None
location_col_index = None

for i, row in df.iterrows():
    for j, val in enumerate(row):
        if str(val).strip() == 'Location':
            location_row_index = i
            location_col_index = j
            break
    if location_row_index is not None:
        break

if location_row_index is None or location_col_index is None:
    raise ValueError("'Location' not found in any cell")

# Slice the DataFrame to remove rows and columns before 'Location'
df = df.iloc[location_row_index:].reset_index(drop=True)
df = df.iloc[:, location_col_index:].copy()

# Promote the first row to headers
df.columns = df.iloc[0].astype(str).str.strip()
df = df[1:].reset_index(drop=True)

# Trim whitespace from all string columns using map
for col in df.columns:
    if df[col].dtype == "object":
        df[col] = df[col].map(lambda x: x.strip() if isinstance(x, str) else x)

#Filter rows where Legacy is not null
filtered_df = df[df['Legacy'].notnull()].copy()

#Split by delimitter
filtered_df['Legacy'] = filtered_df['Legacy'].str.split('/')

#Expand to new rows 
expanded_df = filtered_df.explode('Legacy')

#Trim Legacy column 
expanded_df['Legacy'] = expanded_df['Legacy'].str.strip()

#Replace profit center with Legacy code
expanded_df['SYSTEM Code: Cost Center / Profit Center'] = expanded_df['Legacy']

#Replace Profit Center name with Roll-up (helps elimated duplication) 
expanded_df['SYSTEM Name: Cost Center / Profit Center'] = expanded_df['SYSTEM Name: Cost Center / Profit Center Roll-up']

#Replace Cost Center/Profit Center with SYSTEM code and Name 
expanded_df['Cost Center / Profit Center'] = ( expanded_df['SYSTEM Code: Cost Center / Profit Center'].astype(str) + ": " 
         + expanded_df['SYSTEM Name: Cost Center / Profit Center Roll-up'].astype(str) )

#Replace Location with Cost Center/Profit Center (helps elimated duplication) 
expanded_df['Location'] = expanded_df['Cost Center / Profit Center']

columns_to_keep = [
    "Location",
    "Product Category",
    "Type",
    "SYSTEM Code: Company",
    "SYSTEM Name: Company",
    "SYSTEM Code: Line of Business",
    "SYSTEM Name: Line of Business",
    "SYSTEM Code: Product Category",
    "SYSTEM Name: Product Category",
    "SYSTEM Code: Cost Center / Profit Center Roll-up",
    "SYSTEM Name: Cost Center / Profit Center Roll-up",
    "SYSTEM Code: Contract Parent (Segment)",
    "SYSTEM Name: Contract Parent (Segment)",
    "SYSTEM Code: Cost Center / Profit Center",
    "SYSTEM Name: Cost Center / Profit Center",
    "Company",
    "Cost Center / Profit Center (Roll-up)",
    "Segment",
    "Line of Busines",
    "Cost Center / Profit Center"
]

# Select only the desired columns
selected_df = expanded_df[columns_to_keep]

# Replace NaN with empty string
selected_df = selected_df.fillna("")

# Convert all columns to string (like Power Query does internally)
selected_df = selected_df.astype(str)

# 3. Drop duplicates
distinct_df = selected_df.drop_duplicates().reset_index(drop=True)

# Export to Excel
distinct_df.to_csv(r"C:\Users\<USER>\Downloads\Legacy Hierarchy.csv", index=False)

print("<COMPANY> Legacy Hierarchy has been created.")



