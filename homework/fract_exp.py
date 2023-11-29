import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

# Define the dimensions of the image
width, height = 800, 800

# Define the scale and limits of the fractal
x_min, x_max = -1.5, 1.5
y_min, y_max = -1.5, 1.5

# Generate a grid of complex numbers
x, y = np.linspace(x_min, x_max, width), np.linspace(y_min, y_max, height)
X, Y = np.meshgrid(x, y)
Z = X + 1j * Y

# Julia set parameters
c = -0.7 + 0.27015j  # Parameter for Julia set, can be adjusted
iterations = 300
threshold = 4

# Initialize the image
image = np.zeros((width, height))

# Generate the fractal image
for i in tqdm(range(width)):
    for j in range(height):
        z = Z[j, i]
        for k in range(iterations):
            z = z**2 + c
            if abs(z) > threshold:
                break
        image[j, i] = k

# Plot the image
plt.imshow(image, cmap='hot', extent=[x_min, x_max, y_min, y_max])
plt.colorbar()
plt.title("Julia Set")
plt.show()
