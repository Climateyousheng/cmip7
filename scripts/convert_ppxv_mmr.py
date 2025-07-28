# This file will convert concentration of GHGs (ppm etc) into Mass Mixing Ratio (MMR).
import read_hisGHGs_conc
import helper

df_raw = read_hisGHGs_conc.df_ann_glb

# def to convert the input ppx (ppm, ppb, ppt) into the output of 
# Mixing Mass Ratio (mmr).
# 5 main GHGs could be converted, inc. CO2, CH4, N2O, CFC12eq, HFC134aeq, with
# units of ppm, ppb, ppb, ppt, ppt.

mm_air = 28.97
def ppx_to_mmr_converter(species, ppx_input):
    # Here we expect species to be a single string, and ppx_input to be a list.
    # check for species and molecular mass
    if species=='co2':
        factor=10**(-6)
        mm = 44.01
    elif species=='ch4':
        factor=10**(-9)
        mm = 16.04
    elif species=='n2o':
        factor=10**(-9)
        mm = 44.01
    elif species=='cfc12eq':
        factor=10**(-12)
        mm = 120.91
    elif species=='hfc134aeq':
        factor=10**(-12)
        mm = 102.03
    else:
        print('Species are wrong or not supported now!')
    
    # get the molecular mass from the gas
    mmr_output = []
    for i in range(len(ppx_input)):
        mmr = mm*factor*ppx_input[i]/mm_air
        mmr_output.append(f"{mmr:.3e}")
    
    return mmr_output

# =========================================================================
# CMIP7 data, from input4mips
# Data need to be converted (with original units)
# spe [1850, 1920,  1950,  1960,  1970,  1980,  1990,  2000,  2010,  2022]
# ch4 [798.8,1003.8,1165.0,1263.0,1412.8,1584.0,1720.0,1778.9,1809.7,1922.1]
# n2o [271.6,284.0, 290.6, 292.9, 296.4, 301.7, 308.9, 315.7, 323.2, 355.7]
# cfc [8.2,  10.6,  32.2,  79.4,  234.5, 562.0, 911.3, 1010.6,1012.9,972.8]
# hfc [20.2, 20.5,  23.3,  25.4,  30.3,  43.1,  62.4,  106.1, 203.5, 408.1]
# =========================================================================

cmip7_yrs = [1850, 1920,  1950,  1960,  1970,  1980,  1990,  2000,  2010,  2022]
cmip7_ch4 = [798.8,1003.8,1165.0,1263.0,1412.8,1584.0,1720.0,1778.9,1809.7,1922.1]
cmip7_n2o = [271.6,284.0, 290.6, 292.9, 296.4, 301.7, 308.9, 315.7, 323.2, 355.7]
cmip7_cfc = [8.2,  10.6,  32.2,  79.4,  234.5, 562.0, 911.3, 1010.6,1012.9,972.8]
cmip7_hfc = [20.2, 20.5,  23.3,  25.4,  30.3,  43.1,  62.4,  106.1, 203.5, 408.1]

# conversion
# print(ppx_to_mmr_converter('co2',[280,400],))
# print(ppx_to_mmr_converter('ch4', cmip7_ch4))
# print(ppx_to_mmr_converter('n2o', cmip7_n2o))
# print(ppx_to_mmr_converter('cfc12eq',cmip7_cfc))
# print(ppx_to_mmr_converter('hfc134aeq',cmip7_hfc))

# call fucntion for single ghg block change
# print(helper.format_fortran_ghg_block(2, cmip7_yrs, cmip7_ch4))
# print(helper.format_fortran_ghg_block(3, cmip7_yrs, cmip7_n2o))
# print(helper.format_fortran_ghg_block(5, cmip7_yrs, cmip7_cfc))
# print(helper.format_fortran_ghg_block(11, cmip7_yrs, cmip7_hfc))

# call function for whole ghg block
helper.replace_clim_fcg_blocks(
    "template",
    "clim_fcg_final",
    replacements={
        2: (cmip7_yrs, cmip7_ch4),  # CH4
        # Add others as needed:
        # 1: (co2_yrs, co2_vals),
        3: (cmip7_yrs, cmip7_n2o),
        5: (cmip7_yrs, cmip7_cfc),
        11: (cmip7_yrs, cmip7_hfc)
    }
)