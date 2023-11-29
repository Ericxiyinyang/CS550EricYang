from PIL import Image, ImageDraw
import random

if __name__ == "__main__":
    dimx, dimy = 300, 300
    img = Image.new('RGB', (dimx, dimy), (0, 0, 0))
    for x in range(dimx):
        for y in range(dimy):
            random_y_color = random.randint(0, 255)
            img.putpixel((x, y), (x % 256, random_y_color, 60))
    img.show()

