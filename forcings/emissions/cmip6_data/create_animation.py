import numpy as np
import xarray as xr 
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.util import add_cyclic_point

# def to add cyclic point to a data array
def xr_add_cyclic_point(da):
    """
    Inputs
    da: xr.DataArray with dimensions (t,latitude,longitude)
    """

    # Use add_cyclic_point to interpolate input data
    lon_idx = da.dims.index('longitude')
    wrap_data, wrap_lon = add_cyclic_point(da.values, coord=da.longitude, axis=lon_idx)

    # Generate output DataArray with new data but same structure as input
    outp_da = xr.DataArray(data=wrap_data,
                           coords = {'t': da.t, 'latitude': da.latitude, 'longitude': wrap_lon},
                           dims=da.dims,
                           attrs=da.attrs)

    return outp_da

# load dataset
ds = xr.open_dataset('qrclim.co2.CMIP6_historical.pp.nc')
emi = ds.field1561_ua
emi.attrs = ds.field1561_ua.attrs
emitest = emi

# extract vmin/vmax, lon/lat?
vmin = emi.min().values
vmax = emi.max().values
lon = ds.longitude
lat = ds.latitude
time = ds.t

# animation
fig = plt.figure(figsize=(12,8))
ax = plt.axes(projection=ccrs.Mollweide())
ax.coastlines(linestyle=':', alpha=0.5)
ax.add_feature(cfeature.BORDERS, linestyle='-', alpha=0.2)

# initialize plot
initial_data = xr_add_cyclic_point(emi.isel(t=3000, unspecified=0))
im = plt.contourf(initial_data.longitude, initial_data.latitude, initial_data, 30,
             transform=ccrs.PlateCarree(), cmap='Reds')
cbar = plt.colorbar(orientation='horizontal', label='Emissions')
gl = ax.gridlines(draw_labels=False)
gl.left_labels = True
gl.right_labels = True

# Efficient data handling
emi_cyclic = xr_add_cyclic_point(emi)
data_bucket = [emi_cyclic.isel(t=i, unspecified=0) for i in range(len(time))]

# update function
def update(frame):
    data_plot = data_bucket[frame+3000]
    im.set_array(data_plot.values.ravel())
    ax.set_title(f'Global Emissions: Year {time[frame].values}')
    return im

ani = animation.FuncAnimation(fig, update, frames=len(time)-3000, interval=20)
plt.show()
ani.save('emi_optimized_t01.gif', writer='ffmpeg', fps=30)
