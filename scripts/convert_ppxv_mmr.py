# This file will convert concentration of GHGs (ppm etc) into Mass Mixing Ratio (MMR).
import read_hisGHGs_conc

df_raw = read_hisGHGs_conc.df_ann_glb

# def to convert the input ppx into the output of mmr.
def ppx_to_mmr_converter(ppx_input, unit, mmr_output):
    # check for units and molecular mass
    if unit=='ppm':
        factor=10^(-6)
    elif unit=='ppb':
        factor=10^(-9)
    elif unit=='ppt':
        factor=10^(-12)
    else:
        print('Units are wrong or not supported now!')
    
    # get the molecular mass from the gas
    