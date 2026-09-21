# ## Enterprise Hierarchy Extraction
# 
# This process extracts the current organizational hierarchy from the live hierarchy workbook and creates a reporting-ready lookup table for downstream reporting and analytics.
# 
# Key steps performed:
# 
# - Loads the Master Data worksheet from the hierarchy workbook.
# - Dynamically locates the hierarchy starting point using the `Location` field.
# - Removes introductory rows and columns that are not part of the hierarchy structure.
# - Promotes the identified header row.
# - Cleans whitespace from text fields.
# - Excludes non-reporting hierarchy records.
# - Retains only hierarchy fields required for reporting and analysis.
# - Creates a standardized hierarchy dataset for use in reporting models and data integration processes.
# - Exports the final hierarchy to CSV format.
# 
# ### Included Hierarchy Levels
# 
# The output contains organizational hierarchy attributes including:
# 
# - Company
# - Line of Business
# - Product Category
# - Segment
# - Cost Center / Profit Center
# - Cost Center / Profit Center Roll-Up
# - Location
# 
# ### Data Transformations
# 
# The process:
# 
# - Identifies the hierarchy table dynamically rather than relying on fixed row positions.
# - Removes rows where `Location = "L::"`.
# - Preserves current hierarchy relationships without modifying source mappings.
# - Retains only business-relevant hierarchy columns.
# 
# ### Output
# 
# **Source File:** `All Hierarchy - LIVE.xlsx`
# 
# **Output File:** `All Hierarchy - LIVE.csv`
# 
# **Result:** A clean, standardized hierarchy lookup table containing current organizational reporting relationships for use in Power BI, financial reporting, and data integration processes.

# In[ ]:





# In[3]:


import pandas as pd
# Load Excel file
file_path = r'C:\Users\<USER>\Downloads\All Hierarchy - LIVE.xlsx'
xls = pd.ExcelFile(file_path, engine='openpyxl')
df = xls.parse('Master Data', header=None)

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

#Filter rows where location <> L::
filtered_df = df[df['Location'] != "L::"]

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
selected_df = filtered_df[columns_to_keep]

# Export to Excel
selected_df.to_csv(r"C:\Users\<USER>\Downloads\All Hierarchy - LIVE.csv", index=False)

print("All Hierarchy has been created.")





