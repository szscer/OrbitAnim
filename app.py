def animate_orbits(

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Define orbital parameters
semi_major_axis_AU = 0.0485 # Semi-major axis in AU
num_points = 300 # Number of points for smooth orbit

# Generate circular orbit
theta = np.linspace(0, 2 * np.pi, num_points)
x_orbit = semi_major_axis_AU * np.cos(theta)
y_orbit = semi_major_axis_AU * np.sin(theta)

# Create figure
fig, ax = plt.subplots(figsize=(6,6))
ax.set_xlim(-semi_major_axis_AU*1.2, semi_major_axis_AU*1.2)
ax.set_ylim(-semi_major_axis_AU*1.2, semi_major_axis_AU*1.2)
ax.set_xlabel("X Position (AU)")
ax.set_ylabel("Y Position (AU)")
ax.set_title("Motion of Proxima b around Proxima Centauri")
ax.grid(True)
ax.set_aspect('equal')

# Plot the orbit path
ax.plot(x_orbit, y_orbit, color="blue", linestyle="--", alpha=0.5, label="Orbit Path")

# Plot the star (Proxima Centauri)
ax.scatter(0, 0, color="red", marker="o", s=100, label="Proxima Centauri")

# Plot the moving planet
planet, = ax.plot([], [], 'bo', markersize=8, label="Proxima b")

# Initialization function
def init():
planet.set_data([], [])
return planet,

# Update function for animation
def update(frame):
planet.set_data(x_orbit[frame], y_orbit[frame])
return planet,

# Create animation
ani = animation.FuncAnimation(fig, update, frames=num_points, init_func=init, interval=50, blit=True)

# Show animation
plt.legend()
plt.show()