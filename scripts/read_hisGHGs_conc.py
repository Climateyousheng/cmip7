import pandas as pd
import numpy as np

file = pd.read_csv('../ghgs_in_MMR_global_mean.csv', index_col='v YEARS/GAS >')
print(file)
df_raw_ghgs = pd.ExcelFile('../forcings/GHGs/Supplementary_Table_UoM_GHGConcentrations-1-1-0_annualmeans_v2.xls',engine='xlrd',)
print(df_raw_ghgs.sheet_names)
df_ann_glb = pd.read_excel('../forcings/GHGs/Supplementary_Table_UoM_GHGConcentrations-1-1-0_annualmeans_v2.xls',sheet_name='historical-annualmean-Global',skiprows=20,index_col=0)