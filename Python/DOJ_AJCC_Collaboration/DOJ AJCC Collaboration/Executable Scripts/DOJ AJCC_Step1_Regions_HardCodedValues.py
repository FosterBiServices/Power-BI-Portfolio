#!/usr/bin/env python
# coding: utf-8

# # DOR AJCC REGIONS
# ## Step 1: Generate Regions Reference File
# 
# ## Purpose
# 
# This step creates the Regions.xlsx reference file used throughout the DOR AJCC reporting process.
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
# **APM US\Data and Insights\Documents\Power BI Source Files\DOR-AJCC Collab**
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

REGION_CODE_LOOKUP = {
    "Sacramento Employment and Training Agency": 29,
    "Workforce Investment Board of Solano County": 43,
    "Workforce Development Board of Ventura County": 48,
    "North Central Counties Consortium": 23,
    "Southeast Los Angeles Workforce Development Board": 42,
    "Workforce Development Board of Madera County": 15,
    "San Bernardino County Workforce Development Department": 32,
    "City of Los Angeles Workforce Development Board": 12,
    "Golden Sierra Workforce Development Board": 7,
    "Yolo County Workforce Development Board": 50,
    "Humboldt County Workforce Development Board": 8,
    "South Bay Workforce Investment Board": 45,
    "San Joaquin County Workforce Development Board": 35,
    "Alameda County Workforce Development Board": 1,
    "Mother Lode Workforce Development Board": 20,
    "Northern Rural Training and Employment Consortium": 22,
    "Riverside County Workforce Development Division": 28,
    "San Diego Workforce Partnership": 33
}

REGION_SHORTDESC_LOOKUP = {
    "Alameda County Workforce Development Board": "ALA",
    "City of Los Angeles Workforce Development Board": "LAI",
    "Golden Sierra Workforce Development Board": "GSC",
    "Humboldt County Workforce Development Board": "HUM",
    "North Central Counties Consortium": "NCC",
    "Sacramento Employment and Training Agency": "SAC",
    "San Bernardino County Workforce Development Department": "SBO",
    "San Joaquin County Workforce Development Board": "SJC",
    "South Bay Workforce Investment Board": "SBY",
    "Southeast Los Angeles Workforce Development Board": "SEL",
    "Workforce Development Board of Madera County": "MAD",
    "Workforce Development Board of Ventura County": "VPN",
    "Workforce Investment Board of Solano County": "SOL",
    "Yolo County Workforce Development Board": "YOL",
    "Mother Lode Workforce Development Board": "MLC",
    "Northern Rural Training and Employment Consortium": "NOR",
    "Riverside County Workforce Development Division": "RIV",
    "San Diego Workforce Partnership": "SDC"
}

def normalize_key(value: str) -> str:
    return " ".join(value.split()).casefold()

code_by_key = {
    normalize_key(k): v
    for k, v in REGION_CODE_LOOKUP.items()
}

short_by_key = {
    normalize_key(k): v
    for k, v in REGION_SHORTDESC_LOOKUP.items()
}

all_regions = sorted(
    set(REGION_CODE_LOOKUP)
    | set(REGION_SHORTDESC_LOOKUP)
)

rows = []

for region in all_regions:
    key = normalize_key(region)

    rows.append(
        {
            "REGION LWDB": region,
            "REGION CODE": code_by_key.get(key),
            "REGION SHORT ABBR": short_by_key.get(key)
        }
    )

Result = (
    pd.DataFrame(rows)
    .sort_values(
        "REGION CODE",
        na_position="last"
    )
    .reset_index(drop=True)
)

# Power Query will return this table
Result