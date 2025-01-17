import matplotlib.pyplot as plt
import numpy as np

# Read the data from the file
filename = "biogem_series_misc_ocn_insol.res"  # Replace with your file's name

# Initialize lists to store data
col_list = []
# time = []
# temperature = []
# surT = []
# benT = []
data_list = []
# Open and process the file
with open(filename, "r") as file:
    for line in file:
        # Skip the header or lines starting with non-data content
        #if line.startswith("%") or line.strip() == "":
        #    continue
        if line.startswith("%"):                            # get column names
            col_list = line.split('/')
            col_list = [col.strip() for col in col_list]
            print(col_list)
            #col_list[i] = [[] for i in range(col_list.count())]
            for index, values in enumerate(col_list):
                data_list[index] = []
            continue
        if line.strip() == "":                              # skip blank lines
            continue
        # Parse each line into variables
        for i in range(len(col_list)):
            values = line.split()            
            data_list[i].append(float(values[i]))
            # time.append(float(values[0]))
            # temperature.append(float(values[1]))
            # surT.append(float(values[2]))
            # benT.append(float(values[3]))

# Convert lists to numpy arrays for easier handling
# time = np.array(time)
# temperature = np.array(temperature)
# surT = np.array(surT)
# benT = np.array(benT)
vars = []
for i in range(len(col_list)):
    vars[i] = np.array(data_list[i])

# Plotting the data
plt.figure(figsize=(10, 6))

# Plot each variable
# plt.plot(time, temperature, label="Temperature (°C)", marker='o')
# plt.plot(time, surT, label="_surT (°C)", marker='s')
# plt.plot(time, benT, label="_benT (°C)", marker='^')
for i in range(len(col_list)-1):
    plt.plot(vars[0], vars[i+1], label=col_list[i+1], marker='o')

# Add labels, title, and legend
# plt.xlabel("Time (years)")
# plt.ylabel("Temperature (°C)")
# plt.title("Temperature Variables vs Time")
# plt.legend()
# plt.grid(True)

# Show the plot
plt.tight_layout()
plt.show()


