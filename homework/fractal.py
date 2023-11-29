"""
Eric
November 13th, 2023

Sources:
Interactive Mandelbrot Set to find zoom coordinates - https://math.hws.edu/eck/js/mandelbrot/MB.html
Julia Set Calculation Guide - https://www.youtube.com/watch?v=mg4bp7G0D3sLinks to an external site.
Julia Set Online Plotter to get zoom coordinates - https://sciencedemos.org.uk/julia.php
Burning Ship Fractal for Formula - https://robotmoon.com/burning-ship-fractal/Links to an external site.
Guide on 3D fractals and ray marching (ultimately scrapped due to performance issues) - https://youtu.be/svLzmFuSBhk?si=FKboDeKLbNdFfMa5
SciPy Sobel Edge detection documentation - https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.sobel.html

Reflection:
I started this project by building off of my code for generating a basic mandelbrot set. I then decided that I wanted to use
the Julia set and also the Burning Ship fractal in my images. Initially, I had planned to use python's openGL library to
render 3d fractals, however, I realized that it would be too slow. I initially tried to generate a mandelbulb fractal, but the
result was very noisy. I left a snapshot of the scrapped 3d fractal in my submission, this was ran through a denoiser and I left
my computer on for a long time to render it. This was when I realized that sticking to 2D would be the better choice. To make the
development process efficient, I used the pickle library to save the fractals I generated, so I wouldn't have to wait for them to
generate everytime I tweaked the coloring algorithm. This gave me plenty of time to make three distinct color algorithms.
In the first image, I want to make a run rise using the mandelbrot set, and clouds using the julia set. I used the sobel edge
detection from SciPy to add some interesting coloring to the sun's rays. In the second image, I first plotted the burning ship
fractal, I don't know what struck me, but it really looked like smeared blood. So I used several burning ships to make blood
stains on a white background as well as a julia set on the finger to make it look like a paper-cut hand. In the last picture
I was feeling some of the Christmas spirit kick in since we are getting so close. I found a star like zoom in the mandelbrot
set and developed a Christmas themed coloring algorithm for the image. I used the sigmoid function (usually for ML and not this
kind of stuff) to make the colors more vibrant and bright while also maintaining the fade effect. Creativity, especially painting
isn't my strong suit, but the peer review process definitely helped me formulate the idea for picture 1 & 2. Originally,
picture 1 only featured a colored zoom of the mandelbrot set, and picture 2 was just a simple rendering of the burning ship fractal.
The last thing I wanted to mention is the application of down sampling in this project. Because these sets have such fine
detail, I generate the original image in 2k and down sampled each to 1k for the final picture. Many smartphones actually use this
technique to make their pictures look better, and I think it worked out well for this project.

ALL generation code is in the following pipeline:

generation function -> painting function -> back to generation function for downsampling -> save image

ALL generated fractals follow the following pipeline:

fractal generator method -> pass each cell ot fractal formula method -> return escape time -> store in 2d array with
escape time -> pkl dump the array for faster performance

Have a good day! :)

On my honor, I have neither given nor received unauthorized aid on this assignment.
"""

# import nessacary libraries
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import sys
from PIL import Image, ImageDraw, ImageFont
import pickle
from scipy.ndimage import sobel, rotate
import math

# the mandelbrot function we made in class
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

# julia function, very close to the mandelbrot function but with a custom starting z
def julia_function(z, c, max_iterations):
    for i in range(max_iterations):
        z = z ** 2 + c
        if abs(z) >= 2:
            return i
    return max_iterations

# function to calculate escape time for the burning ship
def burning_ship_function(c, max_iterations):
    # set initial z
    z = complex(0, 0)
    # for max_iterations iterations, calculate z with c
    for i in range(max_iterations):
        # z calculation function
        z = complex(abs(z.real), abs(z.imag)) ** 2 + c
        # if the abs of new z is greater than 2, return the number of iterations it took to get there
        if abs(z) >= 2:
            return i
    # if we have made it out of the loop, lets just say it escaped at max_iterations
    return max_iterations


# function to make a 2d array of the mandelbrot set with its escape time
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


def draw_mand_sunrise(mand_array, max_iterations, img):
    # use the 2d array to calculate image dimensions
    # final_image = Image.new('RGB', (len(mand_array), len(mand_array[0])))
    final_image = img
    # rotate the image 180 degrees
    rot_mand = np.rot90(mand_array, 2)
    # normalize the array for edge detection
    normalized_array = rot_mand / np.max(rot_mand)
    # <-------code from Sobel documentation-------->
    # Apply Sobel filter
    sobel_x = sobel(normalized_array, axis=0)
    sobel_y = sobel(normalized_array, axis=1)
    sobel_magnitude = np.hypot(sobel_x, sobel_y)
    sobel_normalized = sobel_magnitude / np.max(sobel_magnitude) * 255
    # <-------code from Sobel documentation-------->

    # convert the sobel edge detection array into a numpy int array
    sobel_image_array = sobel_normalized.astype(np.uint8)

    # prepare the color codes for blue sky gradient
    sky_top = (0, 76, 153)
    sky_bottom = (135, 206, 235)

    for y in range(len(rot_mand)):
        # Calculate the blend factor between the two colors
        blend = y / len(rot_mand)

        # Blend the two colors to get the color for the current row
        r = int(sky_top[0] * (1 - blend) + sky_bottom[0] * blend)
        g = int(sky_top[1] * (1 - blend) + sky_bottom[1] * blend)
        b = int(sky_top[2] * (1 - blend) + sky_bottom[2] * blend)

        # Draw a horizontal line with the blended color
        for x in range(len(rot_mand[0])):
            final_image.putpixel((x, y), (r, g, b))

        # basically, the gradient will be made line by line before everything else

    # loop through the mandelbrot array provided
    for i in tqdm(range(len(rot_mand))):
        for j in range(len(rot_mand[0])):
            # calculate a color scale based on the inverted value of the color * escape_time/max_iterations
            color_scale = 255 - int(255 * (rot_mand[i][j] / max_iterations))
            # put the scale into a sigmoid function to obtain the final scale
            sigmoid_scale = sigmoid_function(color_scale, 20)
            # if the scale is greater than 0, put the pixel in the image
            if int(255 * sigmoid_scale) > 0:
                # put a gradient on the non-black parts of this set by multiplying a specific yellow by the sigmoid scale
                final_image.putpixel((i, j),
                                     (int(255 * sigmoid_scale), int(233 * sigmoid_scale), int(196 * sigmoid_scale)))
            # if the sobel edge detection is greater than 0, put the pixel in the image
            if sobel_image_array[i][j] > 0:
                sol_constant = sobel_image_array[i][j]
                # paint the pixel with the sobel edge detection + our wanted color
                final_image.putpixel((i, j), (sol_constant + 120, sol_constant + 100, sol_constant + 5))
    # open up an image draw object
    draw = ImageDraw.Draw(final_image)

    # load in our precalcualted julia set
    with open('julia_cloud.pkl', 'rb') as f:
        julia_cloud = pickle.load(f)
    # loop throgugh the julia set
    for i in tqdm(range(len(julia_cloud))):
        for j in range(len(julia_cloud[0])):
            # if the value is greater than 254, put the pixel in the image, giving us a cloud
            if julia_cloud[i][j] > 254:
                final_image.putpixel((i + 360, j - 500), (177, 200, 206))
                final_image.putpixel((i - 500, j - 500), (177, 200, 206))
    #draw simple sun with three circles
    draw.ellipse((330, 385, 1530, 1585), fill=(253, 182, 39))
    draw.ellipse((430, 485, 1430, 1485), fill=(255, 231, 182))
    draw.ellipse((530, 585, 1330, 1385), fill=(253, 253, 225))
    # draw the cloud infront
    for i in tqdm(range(len(julia_cloud))):
        for j in range(len(julia_cloud[0])):
            if julia_cloud[i][j] > 254:
                final_image.putpixel((i - 80, j - 200), (232, 250, 255))

    # draw the mountain by mapping the points and filling
    draw.polygon([(20, 2000), (700, 1100), (1200, 2000)], fill="Green")
    draw.polygon([(720, 2000), (700, 1300), (2000, 2000)], fill="Green")
    draw.polygon([(1500, 2000), (1600, 1300), (2000, 2000)], fill="Green")
    return final_image


def draw_ship_pic(ship_array, max_iterations, img):
    # set the image canvas to final_image
    final_image = img
    # initialize an imagedraw object for the picture frame
    draw = ImageDraw.Draw(final_image)
    draw.rectangle((0, 0, 2000, 2000), fill=(239, 251, 255))

    # loop through the ship array to get pixel data
    for i in tqdm(range(len(ship_array))):
        for j in range(len(ship_array[0])):
            # calculate the color value based on the escape time
            color_value = ship_array[i][j] / max_iterations
            if color_value > 0.1:
                # if the color value is greater than 0.1, put the pixel in the image with just color value 1
                color_value = 1

                # I wanted an inverted red color so I used 255 - 47 * color_value * 1.8 to get a deep red
                final_image.putpixel((int(j / 3 + 320), int(i / 3 + 600)), (
                    int((255 - 47 * color_value * 1.8)), int((255 - 203 * color_value * 1.8)),
                    int((255 - 255 * color_value * 1.8))))
                final_image.putpixel((int(j / 3 + 500), int(i / 3 + 750)), (
                    int(255 - 47 * color_value * 1.8), int(255 - 203 * color_value * 1.8),
                    int(255 - 255 * color_value * 1.8)))
                final_image.putpixel((int(j / 3 + 600), int(i / 3 + 790)), (
                    int(255 - 47 * color_value * 1.8), int(255 - 203 * color_value * 1.8),
                    int(255 - 255 * color_value * 1.8)))
    # once again open the premade julia set
    with open('julia_cloud.pkl', 'rb') as f:
        julia_cloud = pickle.load(f)

    # use scipy's rotate function to rotate the julia set by 10 degress
    julia_rot = rotate(julia_cloud, angle=10)

    # draw the hand with rectangles and circles
    draw.rectangle((0, 0, 2000, 300), fill=(239, 251, 255))
    draw.ellipse((280, 500, 580, 800), fill=(255, 233, 190))
    draw.rectangle((430, 500, 2000, 800), fill=(255, 233, 190))
    # loop through the julia set to draw blood on the hand
    for i in tqdm(range(len(julia_rot))):
        for j in range(len(julia_rot[0])):
            # ONLY draw if it is within the bound of the hand
            if julia_rot[i][j] > 254 and 800 >= j - 200 >= 500:
                final_image.putpixel((i-400, j-200), (135, 13, 13))
    draw.ellipse((1180, 390, 2280, 1490), fill=(224, 206, 169))
    return final_image


def generate_ship_pic():
    # initialize a new PIL image object that is 2k
    burning_ship_image = Image.new('RGB', (2000, 2000))

    # burning ship generation code, uncomment to generate but it takes a while so using the presaved pkl is ideal
    # burning_ship_fractal = generate_burning_ship(2000, 255, -1.765, -1.7825, -0.0671, -0.0494)
    # with open('burning_ship.pkl', 'wb') as f:
    #     pickle.dump(burning_ship_fractal, f)
    # print("dump complete")

    # open the calculated burning ship pkl
    with open('burning_ship.pkl', 'rb') as f:
        burning_ship_fractal = pickle.load(f)

    # draw the ship picture
    ship_pic = draw_ship_pic(burning_ship_fractal, 255, burning_ship_image)

    # downsample the picture to 1k
    ship_pic.thumbnail((1000, 1000))

    # show and also save the picture
    ship_pic.show(title="A Bleeding Hand")
    ship_pic.save("bleedinghand.png")


# helper function to run the sigmoid function with whatever x shift as the argument
def sigmoid_function(x, shift):
    return 1 / (1 + math.exp(-x + shift))

# plot statistics graph of the mandelbrot set, useful for developing coloring algorithms
def draw_mand_2d_num(mand_array, max_iterations):
    # use matplotlib to plot the distribution of the number of iterations it took to escape for each pixel
    plt.hist(mand_array.flatten(), bins=max_iterations)
    plt.show()

# function to generate the burning ship 2d array
def generate_burning_ship(size, max_iterations, x_max, x_min, y_max, y_min):
    # initialize the array
    fractal = np.zeros((size, size))
    # loop through the array
    for i in tqdm(range(size)):
        for j in range(size):
            # calculate the complex number c for each cell by our x and y zooms
            x = j * (x_max - x_min) / (size - 1) + x_min
            y = i * (y_max - y_min) / (size - 1) + y_min
            c = complex(x, y)
            # set the cell to the escape time
            fractal[i][j] = burning_ship_function(c, max_iterations)
    return fractal

# function to generate a 2d array of the julia set
def make_julia_2d(size, c, max_iterations, x_max, x_min, y_max, y_min):
    # initialize the array
    julia_2d = np.zeros((size, size))
    # calculate cell increment
    h_cell_increment = (x_max - x_min) / (size - 1)
    v_cell_increment = (y_max - y_min) / (size - 1)
    # loop through the array
    for i in tqdm(range(size)):
        for j in range(size):
            # calculate the complex number z for each cell
            x = j * h_cell_increment + x_min
            y = i * v_cell_increment + y_min
            z = complex(x, y)
            # set the cell to the escape time
            julia_2d[i][j] = julia_function(z, c, max_iterations)
    return julia_2d

# generation of the sun rise picture
def generate_sun_rise():
    # initialize a new picture
    black_hole_img = Image.new('RGB', (2000, 2000))

    # swirl_mandel generation code, uncomment if you want to wait for it to generate
    # swirl_mandel = make_mand_2d(
    #     2000,
    #     250,
    #     x_max=-0.744046336000000000000,
    #     x_min=-0.745928704000000000000,
    #     y_max=-0.134352384000000000000,
    #     y_min=-0.136234752000000000000
    # )

    # open the presaved pkl file for fast performance
    with open('mand_swirl.pkl', 'rb') as f:
        swirl_mandel = pickle.load(f)

    # draw the sun rise picture
    sun_img = draw_mand_sunrise(swirl_mandel, 255, black_hole_img)
    # down sample the picture to 1k
    sun_img.thumbnail((1000, 1000))
    sun_img.show(title="Mandelbrot Sunrise")
    sun_img.save("sunrise.png")

# generate the Christmas fractal
def generate_christmas():
    # make a new image
    christmas_img = Image.new('RGB', (2000, 2000))

    # christmas mandel generation code (uncomment if you want to wait for it to generate)
    # christmas_mand = make_mand_2d(
    #     2000,
    #     255,
    #     x_max=-1.798907973549867383825,
    #     x_min=-1.798907973550005833465,
    #     y_max=0.000000017042235031823,
    #     y_min=0.000000017042096582183
    # )
    # with open('christmas_mand.pkl', 'wb') as f:
    #     pickle.dump(christmas_mand, f)

    # open the pre-generated mandelbrot set to save time
    with open('christmas_mand.pkl', 'rb') as f:
        christmas_mand = pickle.load(f)

    # draw the christmas fractal
    christmas_img = draw_snowflake_christmas(christmas_mand, 255, christmas_img)
    # down sample the picture to 1k
    christmas_img.thumbnail((1000, 1000))
    christmas_img.show(title="Merry Christmas!")
    christmas_img.save("christmas.png")

# paint the christmas fractal
def draw_snowflake_christmas(base_array, max_iterations, img):
    # set the image canvas to final_image
    final_image = img
    # rotate the image 90 degrees
    rot_mand = np.rot90(base_array, 1)
    # normalize the array for sobel filter
    normalized_array = rot_mand / np.max(rot_mand)

    # Apply Sobel filter, again this is code from the sobel docs
    sobel_x = sobel(normalized_array, axis=0)
    sobel_y = sobel(normalized_array, axis=1)
    sobel_magnitude = np.hypot(sobel_x, sobel_y)
    # normalize the sobel filter by dividing it's magnitude with the max magnitude and multiplying by 255
    sobel_normalized = sobel_magnitude / np.max(sobel_magnitude) * 255
    # convert the sobel edge detection array into a numpy int array
    sobel_image_array = sobel_normalized.astype(np.uint8)

    # loop through the mandelbrot array provided
    for i in tqdm(range(len(rot_mand))):
        for j in range(len(rot_mand[0])):
            # same color scale implementation
            color_scale = 255 - int(255 * (rot_mand[i][j] / max_iterations))
            # put the pixel in the image
            sigmoid_scale = sigmoid_function(color_scale, 105)
            if int(255 * sigmoid_scale) > 0:
                # even = green, odd = red
                if int(255 * sigmoid_scale) % 2 == 0:
                    final_image.putpixel((i, j),
                                     (int(255 * sigmoid_scale), int(83 * sigmoid_scale), int(83 * sigmoid_scale)))
                else:
                    final_image.putpixel((i, j),
                                         (int(113 * sigmoid_scale), int(255 * sigmoid_scale), int(137 * sigmoid_scale)))
            # add outlines
            if sobel_image_array[i][j] > 0:
                final_image.putpixel((i, j), (int(255 * sigmoid_scale), int(255 * sigmoid_scale), int(255 * sigmoid_scale)))
            # inverted star coloring in the center if it is zero
            if int(255 * sigmoid_scale) <= 0:
                final_image.putpixel((i, j),
                                     (255, 255, 255))
    return final_image



if __name__ == "__main__":
    print("If you are seeing this that means the program is running! Please wait.")
    generate_sun_rise()
    generate_ship_pic()
    generate_christmas()
    # size = int(input("Enter the size of the image you want to generate: \n>>>"))
    # x_maxim = float(input("Enter the maximum x value you want to plot: \n>>>"))
    # x_minim = float(input("Enter the minimum x value you want to plot: \n>>>"))
    # y_maxim = float(input("Enter the maximum y value you want to plot: \n>>>"))
    # y_minim = float(input("Enter the minimum y value you want to plot: \n>>>"))
    # mandelbrot_array = make_mand_2d(size, 255, x_maxim, x_minim, y_maxim, y_minim)
    # mandelbrot_array = make_mand_2d(500, 255, -0.4432, -0.5272, 0.6492, 0.5652)
    # draw_mand_2d(mandelbrot_array, 255)
    # draw_mand_2d_num(mandelbrot_array, 255)
    # julia_c = complex(-0.4, 0.6)
    # julia_array = make_julia_2d(2000, julia_c, 255, 1.5, -1.5, 1.5, -1.5)
    # uncomment this to make the julia set cloud pkl file
    # julia_cloud = make_julia_2d(2000, complex(0.0001, 0.6), 255, 3.937213694081, -3.540119639253, 1.926527421914
    #                             , -2.073472578086)
    # with open('julia_cloud.pkl', 'wb') as f:
    #     pickle.dump(julia_cloud, f)

"""
Peer Review - Feedback and Changes

Leon Zhang '25 (tested the 3d, didn't go well at all...):
- The 3D fractal idea is cool, but this result is very noisy and hard to see. 
- (We literally sat in the SAC for 30 minutes to render a less noisy version with more iterations)

Changes made: 
- I started work on a backup 2D project if the 3D does not pan out well.
- Finally this version of the project was scrapped because something taking this long to render
would make tweaking the coloring algorithm very hard.

Leon Zhang '25 (early 2D version):
- The colors are very dark, some vibrance might help
- choose more interesting locations in the fractal...some of these are very generic

Changes made: 
(since this was after the 3D was scrapped, the 2D was in rough shapes)
- I took an ML course last winter and learned about activation functions that map a value to a range. I decided to use
the (at this point outdated) sigmoid function to squash my values down to the curve of the function. With that I got the
coloring I wanted but also the control I wanted.
- I think the final version has a lot more interesting locations in the fractals. I also made sure to make really purposeful
coloring algorithms that is not random. I'm pretty sure you can see the specific colors I chose in each image.

Tye Chokephaibulkit '24 (tested the 2d fractal):
* FULL DISCLOSURE: Tye took this course last year...so he understands the basics of this project *
- The first one is a classic mandelbrot set, maybe something like a sun would look cool with the spiral pattern you found?
- (I don't know how we came to this conclusion) Why does the second one look like a blood wipe? Like the bleeding effect in a game?
- Nice coloring on the first image, but its so generic...maybe add a color palette to the mandelbrot set?

Changes made:
I had a really good time reviewing the fractals with Tye. Here are the changes I made:

1. I decided build a sunrise theme in the first image, this resulted in a very interesting coloring algorithm I developed
using sobel and the sigmoid function shifted by ~30 horizontally. I also used a specific julia set and inverted the escape
time coloring to produce blue clouds.

2. Umm...so this one is a far stretch. The final image is literally a bleeding hand, but hey I also applied the julia set to
this and also the burning ship fractal.

3. So to clarify, the first image was initially just shaded with a yellow gradient. To build the algorithm for Christmas colors
I decided to shade green/red based on if the calculated value is odd/even. I also inverted the center of the set to make a star
white shape. 

Andy Chin '25 (Discussion on downsampling):
- I learned in photography class that a downsampled 1k image looks better than a native 1k image. It's because you are
originally capturing more detail and so the average taken for the downsample is more accurate.

Changes made:
- As you can see in the final code, every image is originally generated in 2k and then downsampled to 1k for the final image.

"""