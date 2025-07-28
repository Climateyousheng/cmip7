import re

# GHG index mapping for readability (optional)
GHG_INDEX = {
    "co2": 1,
    "ch4": 2,
    "n2o": 3,
    "cfc12eq": 5,
    "hfc134aeq": 11
}


# ===========================================================
# This allows us to produce a single ghg block in the CNTLATM
# ===========================================================
def format_fortran_ghg_single_block(index, years, values, varname="CLIM_FCG", values_are_ppb=True, per_line=4):
    assert len(years) == len(values)
    n = len(years)

    if values_are_ppb:
        values = [v * 1e-9 for v in values]  # Convert ppb to mole fraction

    def format_list(lst, fmt=str):
        formatted = [fmt(x) for x in lst]
        lines = []
        for i in range(0, len(formatted), per_line):
            chunk = formatted[i:i+per_line]
            line = ",".join(chunk)
            lines.append(" " + line)
        return "\n".join(lines)

    # Format sections
    years_block = format_list(years, str)
    levls_block = format_list(values, lambda x: f"{x:.6e}")
    rates_block = format_list(["-32768.0"] * n)

    return (
        f"{varname}_NYEARS({index})={n},\n"
        f"{varname}_YEARS(1,{index})=\n{years_block},\n"
        f"{varname}_LEVLS(1,{index})=\n{levls_block},\n"
        f"{varname}_RATES(1,{index})=\n{rates_block}"
    )
# Example usage
# print(format_fortran_ghg_block(2, cmip7_yrs, cmip7_ch4))  # for CH₄
# ===========================================================


# ===========================================================
# This is the full function for all ghg blocks in the CNTLATM
# ===========================================================
def format_fortran_ghg_block(index, years, values, values_are_ppb=True, max_line_length=100):
    if values_are_ppb:
        values = [v * 1e-9 for v in values]

    def format_lines(label, index_str, values_list, formatter=str):
        head = f" {label}({index_str})="
        lines = []
        current_line = head
        first_value = True

        for i, v in enumerate(values_list):
            part = formatter(v)
            if len(current_line) + len(part) + (0 if first_value else 1) > max_line_length:
                lines.append(current_line)
                current_line = " " + part
                first_value = False
            else:
                if not first_value:
                    current_line += ","
                current_line += part
                first_value = False

        lines.append(current_line)
        return "\n".join(lines)

    n = len(years)
    block = [
        f" CLIM_FCG_NYEARS({index})={n},",
        format_lines("CLIM_FCG_YEARS", f"1,{index}", years, str) + ",",
        format_lines("CLIM_FCG_LEVLS", f"1,{index}", values, lambda x: f"{x:.6e}") + ",",
        format_lines("CLIM_FCG_RATES", f"1,{index}", ["-32768.0"] * n) + ","
    ]
    return "\n".join(block)




def replace_clim_fcg_blocks(input_path, output_path, replacements):
    target_indices = {1, 2, 3, 5, 11}
    lines = open(input_path).readlines()
    result = []
    i = 0
    skip_mode = False
    current_index = None

    while i < len(lines):
        line = lines[i]
        nyears_match = re.match(r'\s*CLIM_FCG_NYEARS\((\d+)\)=', line)
        if nyears_match:
            current_index = int(nyears_match.group(1))
            if current_index in replacements:
                # Replace the full block
                years, values = replacements[current_index]
                result.append(format_fortran_ghg_block(current_index, years, values))
                skip_mode = True
                i += 1
                continue

        if skip_mode:
            # Skip until the next CLIM_FCG_NYEARS or &END
            if re.match(r'\s*CLIM_FCG_NYEARS\(\d+\)=', line) or line.strip().startswith("&END"):
                skip_mode = False
                continue
            i += 1
            continue

        result.append(line.rstrip())
        i += 1

    with open(output_path, "w") as f:
        f.write("\n".join(result) + "\n")
# Example usage
# Input: replacement only for CH4
# cmip7_ch4_yrs = [1850, 1920, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2022]
# cmip7_ch4_ppb = [798.8, 1003.8, 1165.0, 1263.0, 1412.8, 1584.0, 1720.0, 1778.9, 1809.7, 1922.1]

# replace_clim_fcg_blocks(
#     input_path="clim_fcg_template.txt",
#     output_path="clim_fcg_final.txt",
#     replacements={
#         2: (cmip7_ch4_yrs, cmip7_ch4_ppb),  # CH4
#         # Add others as needed:
#         # 1: (co2_yrs, co2_vals),
#         # 3: (n2o_yrs, n2o_vals),
#         # 5: (cfc_yrs, cfc_vals),
#         # 11: (hfc_yrs, hfc_vals)
#     }
# )
# ===========================================================