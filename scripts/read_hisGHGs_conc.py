import os
import pandas as pd
import numpy as np

# Make sure the path is correct
print("Current Directory:", os.getcwd())
# base_dir = os.path.dirname(os.path.abspath(__file__))         # Directory of this script

# Load the file
if os.path.exists('../forcings/GHGs'):
    try:
        file_path = os.path.join(os.getcwd(),'../forcings/GHGs/Supplementary_Table_UoM_GHGConcentrations-1-1-0_annualmeans_v2.xls')
        df_raw_ghgs = pd.ExcelFile(file_path, engine='xlrd')
        print("File loaded successfully!")
    except Exception as e:
        print(f"Error reading the Excel file: {e}")
else:
    print(f"Directory does not exist: {os.getcwd()+'../forcings/GHGs'}")

# Process the exact sheet from the file we are interested in
print(f"Available sheets including {df_raw_ghgs.sheet_names}")  # Get sheet names
# Read the historical global annual mean data
df_ann_glb_raw = pd.read_excel(file_path, sheet_name='historical-annualmean-Global', header=None)
# postprocess
units = df_ann_glb_raw.iloc[20]                                 # Units (ppm, ppb, etc.)
gases = df_ann_glb_raw.iloc[21]                                 # Gas names (CO2, CH4, etc.)
df_ann_glb = df_ann_glb_raw.iloc[22:].reset_index(drop=True)    # skip 21 rows non-data   
df_ann_glb.columns = df_ann_glb_raw.iloc[21]                    # set gases as columns
df_ann_glb = df_ann_glb.set_index('v YEARS/GAS >')              # set years as index
df_ann_glb = df_ann_glb.rename_axis(index='Years')              # rename the index
print(df_ann_glb.columns)

# save the file
df_ann_glb.to_csv("../forcings/GHGs/his_GHGs_ann_CMIP6.csv",)