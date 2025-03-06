import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#Parameters
semi_major_axis_AU = 0.2 # Semi-major axis in AU
num_points = 50 # Number of points for smooth orbit
g = 39.478
star_mass = 20 #solar masses
eccentricity = 0.8

#compute semi-minor axis
semi_minor_axis_AU = semi_major_axis_AU * np.sqrt(1 - eccentricity**2)

#Generate true anomaly (theta values)
theta = np.linspace(0, 2 * np.pi, num_points)
r = (semi_major_axis_AU * (1 - eccentricity**2)) / (1 + eccentricity * np.cos(theta))
x_orbit = r * np.cos(theta)
y_orbit = r * np.sin(theta)

# Compute orbital speed using Kepler's laws (vis-viva equation)
# v^2 = G * M * (2/r - 1/a)
v_orbit = np.sqrt(g * star_mass * (2 / r - 1 / semi_major_axis_AU))

# Normalize time intervals based on speed (faster speed = shorter time interval)
dt = 1 / v_orbit  # Time step inversely proportional to speed
dt /= np.sum(dt)  # Normalize
cumulative_time = np.cumsum(dt)
cumulative_time /= cumulative_time[-1]  # Normalize to range [0,1]

# Interpolate for smooth animation frame selection
from scipy.interpolate import interp1d
frame_interp = interp1d(cumulative_time, np.arange(num_points), kind='linear')

# Set up the figue and axis
fig, ax = plt.subplots(figsize=(6,6))
ax.set_xlim(-semi_major_axis_AU*2.0, semi_major_axis_AU*2.0)
ax.set_ylim(-semi_major_axis_AU*2.0, semi_major_axis_AU*2.0)
ax.set_xlabel("X Position (AU)")
ax.set_ylabel("Y Position (AU)")
ax.set_title("2D Elliptical Orbit with variable speed")
ax.grid(True)
ax.set_aspect('equal')
ax.plot(x_orbit, y_orbit, color="blue", linestyle="--", alpha=0.5, label="Orbit Path")
ax.scatter(0, 0, color="red", marker="o", s=100, label="Star")

# Plot the moving planet
planet, = ax.plot([], [], 'bo', markersize=8, label="Planet")

# Animation function
def update(frame):
    # Normalize frame to range [0, 1]
    normalized_frame = frame / num_points
    # Ensure normalized_frame is within the valid range of cumulative_time
    normalized_frame = np.clip(normalized_frame, cumulative_time.min(), cumulative_time.max())
    true_frame = int(frame_interp(normalized_frame))
     # Ensure true_frame is within the valid range of indices
    true_frame = np.clip(true_frame, 0, len(x_orbit) - 1)
    planet.set_data(x_orbit[true_frame], y_orbit[true_frame])
    return planet,

# Create animation
ani = animation.FuncAnimation(fig, update, frames=num_points, interval=50, blit=True)

# Show animation
from IPython.display import HTML
HTML(ani.to_jshtml())