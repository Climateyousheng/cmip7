import matplotlib.pyplot as plt
import read_hisGHGs_conc

data = read_hisGHGs_conc.file
fig, ax = plt.subplots(ncols=1,nrows=1,figsize=(12,6))
sc = ax.scatter('data.CO2','data.v YEARS/GAS >')
fig.show()
