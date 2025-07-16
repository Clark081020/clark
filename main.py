
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.collections import LineCollection

def calculate_deflection(x, y, bh_x, bh_y, mass, intensity):
    dx = bh_x - x
    dy = bh_y - y
    distance_sq = dx**2 + dy**2
    distance = np.sqrt(distance_sq)
    
    if distance < mass * 0.6:  # Schwarzschild radius
        return 0, 0
    
    deflection = intensity * mass / distance_sq
    return dx * deflection, dy * deflection

def generate_light_ray(start_x, start_y, width, height, bh_x, bh_y, mass, intensity, steps=150):
    x, y = start_x, start_y
    ray_path = [(x, y)]
    
    if start_x == 0:  # Coming from left
        dx, dy = 5, 0
    else:  # Coming from top
        dx, dy = 0, 5
    
    for _ in range(steps):
        deflection_x, deflection_y = calculate_deflection(x, y, bh_x, bh_y, mass, intensity)
        dx += deflection_x
        dy += deflection_y
        
        # Normalize direction
        length = np.sqrt(dx**2 + dy**2)
        dx = (dx / length) * 5
        dy = (dy / length) * 5
        
        x += dx
        y += dy
        ray_path.append((x, y))
        
        if x < 0 or x > width or y < 0 or y > height:
            break
            
    return np.array(ray_path)

def main():
    st.set_page_config(page_title="Gravity Lens Simulator", layout="wide")
    st.title("🌌 Black Hole Gravitational Lensing")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.header("Controls")
        mass = st.slider("Black Hole Mass", 30, 120, 80)
        intensity = st.slider("Warp Intensity", 0.5, 3.0, 1.5, 0.1)
        ray_count = st.slider("Light Rays", 5, 30, 12)
        show_grid = st.checkbox("Show Spacetime Grid", value=True)
        show_photon = st.checkbox("Show Photon Sphere", value=True)
        bh_x = st.slider("Black Hole X", 100, 700, 400)
        bh_y = st.slider("Black Hole Y", 100, 500, 300)
        
    with col2:
        st.header("Simulation")
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.set_xlim(0, 800)
        ax.set_ylim(0, 600)
        ax.set_facecolor('#0a0a20')
        ax.axis('off')
        
        # Draw spacetime grid
        if show_grid:
            grid_size = 40
            for x in np.arange(0, 801, grid_size):
                grid_line = []
                for y in np.arange(0, 601, 5):
                    def_x, def_y = calculate_deflection(x, y, bh_x, bh_y, mass, intensity)
                    grid_line.append([x + def_x, y + def_y])
                ax.plot(*zip(*grid_line), color='rgba(100, 200, 255, 0.3)', linewidth=1)
                
            for y in np.arange(0, 601, grid_size):
                grid_line = []
                for x in np.arange(0, 801, 5):
                    def_x, def_y = calculate_deflection(x, y, bh_x, bh_y, mass, intensity)
                    grid_line.append([x + def_x, y + def_y])
                ax.plot(*zip(*grid_line), color='rgba(100, 200, 255, 0.3)', linewidth=1)
        
        # Draw light rays
        vertical_spacing = 600 / (ray_count + 1)
        horizontal_spacing = 800 / (ray_count + 1)
        
        rays = []
        for i in range(1, ray_count + 1):
            # Rays from left
            ray = generate_light_ray(0, i * vertical_spacing, 800, 600, bh_x, bh_y, mass, intensity)
            rays.append(ray)
            
            # Rays from top
            ray = generate_light_ray(i * horizontal_spacing, 0, 800, 600, bh_x, bh_y, mass, intensity)
            rays.append(ray)
        
        # Create line collection for better performance
        lc = LineCollection(rays, colors='yellow', alpha=0.6, linewidths=1.5)
        ax.add_collection(lc)
