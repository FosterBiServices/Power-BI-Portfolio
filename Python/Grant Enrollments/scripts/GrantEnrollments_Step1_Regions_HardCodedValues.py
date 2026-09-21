# # Grant Enrollments REGIONS
# ## Step 1: Generate Regions Reference File
# 
# ## Purpose
# 
# This step creates the Regions.xlsx reference file used throughout the Grant Enrollments reporting process.
# 
# The file provides a standardized mapping between:
# 
# - Local Workforce Development Board (LWDB) names
# - Region codes
# - Region abbreviations
# 
# This reference data is used to support consistent reporting, joins, filtering, and regional analysis within Power BI and downstream validation processes.
# 
# ## Data Source
# 
# The region mappings are maintained as hardcoded business reference values within this notebook.
# 
# Two lookup tables are defined:
# 
# - Region Code Lookup: Maps each LWDB to its official region code.
# - Region Short Abbreviation Lookup: Maps each LWDB to its reporting abbreviation.
# 
# ## Processing Logic
# 
# The script performs the following actions:
# 
# - Defines the region code and abbreviation lookup dictionaries.
# - Normalizes region names to ensure consistent matching regardless of spacing or capitalization.
# - Combines all regions from both lookup sources.
# - Creates a standardized reference table containing:
# - Region LWDB
# - Region Code
# - Region Short Abbreviation
# - Sorts the output by Region Code.
# - Writes the results to an Excel file named Regions.xlsx.
# 
# ## Output Schema
# 
# ### Column Description
# - REGION LWDB	
#   - Full Local Workforce Development Board name
# - REGION CODE	
#   - Numeric region identifier
# - REGION SHORT ABBR	
#   - Short reporting abbreviation
#     
# ## Output Location
# 
# The generated file is written to the shared Power BI source file location:
# **Users\<USER>\Downloads\Grant Enrollments**
# 
# ## Expected Outcome
# 
# - A single Regions.xlsx file is generated containing one record per region.
# - The resulting file acts as the authoritative regional reference table used by subsequent validation and reporting processes.
# 
# ## Maintenance Notes
# 
# ### When a new region is added or an existing region definition changes:
# 
# 1. Update both lookup dictionaries as required.
# 2. Verify that each region has a valid Region Code and Region Short Abbreviation.
# 3. Regenerate the Regions.xlsx file before refreshing downstream reporting assets.

# 

# In[3]:


import pandas as pd
import os
from pathlib import Path

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

REGION_SHORTDESC_LOOKUP = {
    "Alameda Workforce Board": "ALA",
    "Prairie Glen Workforce Board": "PGW",
    "Amberfield Workforce Board": "AMB",
    "Lakebridge Workforce Board": "LAK",
    "Maple Crossing Workforce Board": "MAP",
    "Rivermoor Workforce Board": "RIV",
    "Pine Hollow Workforce Board": "PIN",
    "Oakmere Workforce Board": "OAK",
    "Clearfork Workforce Board": "CLR",
    "Grand Meadow Workforce Board": "GRM",
    "Silver Creek Workforce Board": "SLV",
    "Redstone Workforce Board": "RED",
    "Elm Harbor Workforce Board": "ELM",
    "Stonefield Workforce Board": "STN",
    "Briar Lake Workforce Board": "BRL",
    "Westhaven Workforce Board": "WES",
    "Meadowbrook Workforce Board": "MEA"
}

# 🧼 Normalize text keys to prevent mismatches --
def normalize_key(value: str) -> str:
    return " ".join(value.split()).casefold()

code_by_key = {normalize_key(k): v for k, v in REGION_CODE_LOOKUP.items()}
short_by_key = {normalize_key(k): v for k, v in REGION_SHORTDESC_LOOKUP.items()}

# Union of all regions from both dictionaries
all_regions = sorted(set(REGION_CODE_LOOKUP) | set(REGION_SHORTDESC_LOOKUP))

rows = []
for region in all_regions:
    key = normalize_key(region)
    rows.append({
   "REGION LWDB": region,
   "REGION CODE": code_by_key.get(key),
   "REGION SHORT ABBR": short_by_key.get(key)
    })

region_df = (
    pd.DataFrame(rows)
 .sort_values("REGION CODE", na_position="last")
 .reset_index(drop=True)
)


# User home directory (dynamic)
home_dir = Path.home()

# SharePoint relative path inside OneDrive
sharepoint_relative_path = Path(
    "<COMPANY>",
    "<SITE>",
    "<PARENT>",
    "<CHILD>",
    "<CHILD2>"
)

target_dir = home_dir / sharepoint_relative_path

# 📁 Ensure the folder exists
target_dir.mkdir(parents=True, exist_ok=True)

# 📁 Full path with name for output file 
output_path = rf'{target_dir}\Regions.xlsx'

# ✍ Write to new file
with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
    region_df.to_excel(writer, sheet_name="REGIONS", index=False)

# 🏁 Completion message
print(f"✅ Mapping complete. File written to:\n{output_path}")





