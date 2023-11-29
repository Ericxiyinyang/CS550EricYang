"""
Eric
October 30th, 2023

Sources:
None

Reflection:
Functions are really important for this homework assignment, and I made sure to build this in such a way that you can get
any resolution you want by changing just one parameter. Everything else, including the increments and the colors are calculated
directly without any other input. I also made sure to use the tqdm library to show a progress bar so the user will know when
the mandelbrot is done. Initially I worked on this in matplotlib, but I switched the final version over to PIL.


Have a good day! :)

On my honor, I have neither given nor received unauthorized aid on this assignment.
"""


import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import sys
from PIL import Image


def mandelbrot_function(c, max_iterations):
    # set initial z
    z = complex(0, 0)
    # for #max_iterations iterations, calculate z with c
    for i in range(1, max_iterations):
        z = z ** 2 + c
        # if the abs of new z is greater than 2, return the number of iterations it took to get there
        if abs(z) >= 2:
            return i
    # if the abs of new z is never greater than 2, return the max_iterations
    return max_iterations

def make_mand_2d(size, max_iterations, x_max=2.0, x_min=-2.0, y_max=2.0, y_min=-2.0):
    # make new numpy array that is the size of the image
    mandel_2d = np.zeros((size, size))
    # calculate the increment for each cell
    h_cell_increment = (x_max - x_min) / (size - 1)
    v_cell_increment = (y_max - y_min) / (size - 1)
    for i in tqdm(range(size)):
        for j in range(size):
            # for each cell, calculate the complex number c
            x = j * h_cell_increment + x_min
            y = i * v_cell_increment + y_min
            c = complex(x, y)
            mandel_2d[i][j] = mandelbrot_function(c, max_iterations)
    # plot the mandelbrot set
    # plt.imshow(mandel_2d, cmap='Blues_r', interpolation='nearest')
    # plt.show()
    return mandel_2d

def draw_mand_2d(mand_array, max_iterations):
    # use the 2d array to calculate image dimensions
    final_image = Image.new('RGB', (len(mand_array), len(mand_array[0])))
    rot_mand = np.rot90(mand_array, 2)
    for i in tqdm(range(len(rot_mand))):
        for j in range(len(rot_mand[0])):
            # calculate the color of each pixel based on the number of iterations it took to escape
            red_grad_color = int(180 * (rot_mand[i][j] / max_iterations))
            blue_grad_color = int(230 * (rot_mand[i][j] / max_iterations))
            green_grad_color = int(230 * (rot_mand[i][j] / max_iterations))
            # put the pixel in the image
            final_image.putpixel((j, i), (red_grad_color, blue_grad_color, green_grad_color))
    final_image.show()

def draw_mand_2d_num(mand_array, max_iterations):
    # use matplotlib to plot the distribution of the number of iterations it took to escape for each pixel
    plt.hist(mand_array.flatten(), bins=max_iterations)
    plt.show()

if __name__ == "__main__":
    # size = int(input("Enter the size of the image you want to generate: \n>>>"))
    # x_maxim = float(input("Enter the maximum x value you want to plot: \n>>>"))
    # x_minim = float(input("Enter the minimum x value you want to plot: \n>>>"))
    # y_maxim = float(input("Enter the maximum y value you want to plot: \n>>>"))
    # y_minim = float(input("Enter the minimum y value you want to plot: \n>>>"))
    # mandelbrot_array = make_mand_2d(size, 255, x_maxim, x_minim, y_maxim, y_minim)
    mandelbrot_array = make_mand_2d(500, 255, -0.4432, -0.5272, 0.6492, 0.5652)
    # draw_mand_2d(mandelbrot_array, 255)
    draw_mand_2d_num(mandelbrot_array, 255)




