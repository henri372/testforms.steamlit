import streamlit as st
import numpy as np
from PIL import Image

def mandelbrot(c, max_iter):
    z = c
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return max_iter

def generate_mandelbrot(width, height, zoom, max_iter):
    x_min, x_max = -2.5 / zoom, 1.5 / zoom
    y_min, y_max = -2.0 / zoom, 2.0 / zoom
    
    # Generate the Mandelbrot set
    mandelbrot_set = np.zeros((width, height))
    for x in range(width):
        for y in range(height):
            zx = x * (x_max - x_min) / (width - 1) + x_min
            zy = y * (y_max - y_min) / (height - 1) + y_min
            c = complex(zx, zy)
            mandelbrot_set[x, y] = mandelbrot(c, max_iter)
    
    return mandelbrot_set

# Streamlit app title
st.title("Mandelbrot Fractal Generator")

# User input for fractal parameters
width = st.slider("Width", min_value=100, max_value=1000, value=500)
height = st.slider("Height", min_value=100, max_value=1000, value=500)
zoom = st.slider("Zoom", min_value=1, max_value=100, value=50)
max_iter = st.slider("Max Iterations", min_value=50, max_value=500, value=200)

# Generate button
if st.button("Generate"):
    # Generate the Mandelbrot fractal
    mandelbrot_img = generate_mandelbrot(width, height, zoom, max_iter)

    # Convert the Mandelbrot array to an image
    mandelbrot_img = mandelbrot_img / np.max(mandelbrot_img) * 255
    mandelbrot_img = Image.fromarray(mandelbrot_img.astype(np.uint8)).convert("RGB")

    # Display the Mandelbrot fractal image
    st.image(mandelbrot_img, caption="Mandelbrot Fractal", use_column_width=True)
