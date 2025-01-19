import matplotlib.pyplot as plt
import numpy as np
import os
import re

def read_file(filename):
    # Read the data from the file
    print(f'Reading from {os.getcwd()}')
    print(f'Reading file {filename}')
    # Initialize lists to store data
    col_list = []
    data_list = []
    units_list = []
    vars = []
    
    # Open and process the file
    with open(filename, "r") as file:
        print('opened successfully')
        for line in file:
            # Skip the header or lines starting with non-data content
            if line.startswith(" %"):                            # get column names
                col_list = line.split('/')
                col_list = [col.strip(' %') for col in col_list]
                print(f'Variables are {col_list}')
                units_list = [match.group(1) for item in col_list if (match := re.search(r'\(([^)]+)\)', item))]
                for index, values in enumerate(col_list):
                    data_list.append([])                        # create list for columns
                continue
            if line.strip() == "":                              # skip blank lines
                continue
            # Parse each line into variables
            for i in range(len(col_list)):
                values = line.split()            
                data_list[i].append(float(values[i]))

    # Convert lists to numpy arrays for easier handling
    for i in range(len(col_list)):
        vars.append(np.array(data_list[i]))
    print(f'Units are {units_list}')
    print(f'Data overview: {vars}')
    # Return vars
    #return col_list, units_list, vars

def plot_timeseries(filename, col_index):
    # Read the data from the file
    # Initialize lists to store data
    col_list = []
    data_list = []
    units_list = []
    vars = []
    
    # Open and process the file
    with open(filename, "r") as file:
        for line in file:
            # Skip the header or lines starting with non-data content
            if line.startswith(" %"):                            # get column names
                col_list = line.split('/')
                col_list = [col.strip(' %') for col in col_list]
                units_list = [match.group(1) for item in col_list if (match := re.search(r'\(([^)]+)\)', item))]
                for index, values in enumerate(col_list):
                    data_list.append([])                        # create list for columns
                continue
            if line.strip() == "":                              # skip blank lines
                continue
            # Parse each line into variables
            for i in range(len(col_list)):
                values = line.split()            
                data_list[i].append(float(values[i]))

    # Convert lists to numpy arrays for easier handling
    for i in range(len(col_list)):
        vars.append(np.array(data_list[i]))
        if units_list[i]=='degree C':
            vars[i] = np.round(vars[i],2)

    # print time series of the ith variables in col_list
    plt.figure(figsize=(10, 6))
    plt.plot(vars[0], vars[col_index], label=col_list[col_index], marker='o')
    # Add labels, title, and legend
    plt.xlabel(col_list[0])
    plt.ylabel(col_list[col_index])
    plt.title(col_list[col_index]+' against '+col_list[0])
    plt.legend()
    plt.grid(True)

    # Show the plot
    plt.tight_layout()
    plt.show()