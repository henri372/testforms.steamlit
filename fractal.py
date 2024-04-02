import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def generate_ifs_fractal(num_points=50000, num_iterations=1000):
    # Define transformation functions for the IFS fractal
    transformations = [
        (0.85, 0.04, 0.0, 0.85, 0.0, 1.6),  # Transformation 1
        (0.20, -0.26, 0.23, 0.22, 0.0, 1.6),  # Transformation 2
        (-0.15, 0.28, 0.26, 0.24, 0.0, 0.44),  # Transformation 3
        (0.0, 0.0, 0.0, 0.16, 0.0, 0.0)  # Transformation 4
    ]

    # Initialize points
    points = np.zeros((num_points, 2))
    points[0] = [0, 0]

    # Apply transformations
    for i in range(1, num_points):
        # Choose a random transformation
        trans_idx = np.random.choice(len(transformations), p=[0.85, 0.07, 0.07, 0.01])
        a, b, c, d, e, f = transformations[trans_idx]
        x, y = points[i - 1]
        points[i] = [a*x + b*y + e, c*x + d*y + f]

    # Extract x and y coordinates
    x_coords, y_coords = points[:, 0], points[:, 1]

    # Plot the fractal
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.scatter(x_coords, y_coords, color='green', s=0.1)
    ax.axis('off')  # Turn off axes
    ax.set_title('IFS Fractal')
    
    # Show plot
    st.pyplot(fig)

# Streamlit app title
st.title("IFS Fractal Generator")

# Generate and display the fractal
generate_ifs_fractal()
