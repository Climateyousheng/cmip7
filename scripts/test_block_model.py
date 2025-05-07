import numpy as np
import matplotlib.pyplot as plt

# Model parameters
grid_size = 5
uplift_rate = 0.01  # m/year
k = 0.001           # Erodibility constant
m = 0.5             # Discharge exponent
n = 1.0             # Slope exponent
time_steps = 100    # Number of years

# Initialize grid (elevation)
elevation = np.random.rand(grid_size, grid_size)  # Random initial elevation
drainage_area = np.ones_like(elevation)          # Uniform drainage area (simplified)

# Function to calculate slope
def calculate_slope(elevation):
    slope = np.zeros_like(elevation)
    for i in range(1, grid_size - 1):
        for j in range(1, grid_size - 1):
            slope[i, j] = max(
                abs(elevation[i, j] - elevation[i-1, j]),  # Up
                abs(elevation[i, j] - elevation[i+1, j]),  # Down
                abs(elevation[i, j] - elevation[i, j-1]),  # Left
                abs(elevation[i, j] - elevation[i, j+1])   # Right
            )
    return slope

# Time-stepping
for t in range(time_steps):
    slope = calculate_slope(elevation)  # Calculate slope
    erosion = k * (drainage_area**m) * (slope**n)  # Fluvial erosion
    elevation += uplift_rate - erosion             # Update elevation

# Plot final topography
plt.figure(figsize=(8, 6))
plt.imshow(elevation, cmap='terrain', origin='lower')
plt.colorbar(label="Elevation (m)")
plt.title("Final Topography After 100 Years")
plt.show()
