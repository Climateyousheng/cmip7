import matplotlib.pyplot as plt
import read_hisGHGs_conc as data

# Define groups of gases
group1 = ['CH4', 'CFC-12-eq']  # Group 1
group2 = ['CO2', 'N2O', 'HFC-134a-eq']  # Group 2

years = data.df_ann_glb.index  # X-axis (Years)
data_group1 = data.df_ann_glb[group1]  # Data for group 1
data_group2 = data.df_ann_glb[group2]  # Data for group 2

# Define years to mark (every 30 years starting from 1850)
marker_years = range(1850, int(years.max()) + 1, 30)

# Create the plot
fig, ax_main = plt.subplots(figsize=(14, 8))
ax_group2 = ax_main.twinx()  # Create a secondary axis for group 2

# Define colors for groups
color_group1 = ['tab:blue', 'tab:orange']
color_group2 = ['tab:green', 'tab:red', 'tab:purple']

# Plot group 1 gases with markers
for idx, var in enumerate(group1):
    ax_main.plot(years, data_group1[var], linestyle='-', color=color_group1[idx], alpha=0.8, label=var, linewidth=2)
    ax_main.scatter(
        [y for y in marker_years if y in years],
        data_group1.loc[[y for y in marker_years if y in years], var],
        marker='o',
        color=color_group1[idx],
        s=100,  # Marker size
        edgecolor='black',
        label=f'{var} (markers)',
    )
    # Add a special circle for the year 2014
    ax_main.scatter(2014, data_group1.loc[2014, var], marker='o', color=color_group1[idx], s=100, edgecolor='black',)

# Plot group 2 gases with markers on secondary axis
for idx, var in enumerate(group2):
    ax_group2.plot(years, data_group2[var], linestyle='--', color=color_group2[idx], alpha=0.8, label=var, linewidth=2)
    ax_group2.scatter(
        [y for y in marker_years if y in years],
        data_group2.loc[[y for y in marker_years if y in years], var],
        marker='o',
        color=color_group2[idx],
        s=100,  # Marker size
        edgecolor='black',
        label=f'{var} (markers)',
    )
    # Add a special circle for the year 2014
    ax_group2.scatter(2014, data_group2.loc[2014, var], marker='o', color=color_group2[idx], s=100, edgecolor='black',)

# Labels and titles
ax_main.set_ylabel("Group 1 Concentrations", fontsize=14)
ax_group2.set_ylabel("Group 2 Concentrations", fontsize=14)
ax_main.set_xlabel("Year", fontsize=14)
ax_main.set_title("GHGs Concentrations Over 1850-2014", fontsize=16)

# Customize x-axis ticks
ax_main.set_xticks(range(int(years.min()), int(years.max()) + 1, 20))  # Tick every 20 years
ax_main.tick_params(axis='x', rotation=45, labelsize=12)
ax_main.tick_params(axis='y', labelsize=12)
ax_group2.tick_params(axis='y', labelsize=12)

# Legends
ax_main.legend(loc='upper left', bbox_to_anchor=(1.05, 1), fontsize=12, title="Group 1", frameon=False)
ax_group2.legend(loc='upper left', bbox_to_anchor=(1.05, 0.7), fontsize=12, title="Group 2", frameon=False)

# Adjust layout to prevent clipping of labels
plt.tight_layout()

# Show the plot
plt.show()

