from PIL import Image, ImageDraw
import random


stream_deltas = [(1, 0), (-1, 0), (0, 1)]

def draw_stream(stream_img, start_x, start_y, dimx, dimy, r, g, b):
    current_x, current_y = start_x, start_y
    print(f"{current_x}, {current_y}")
    while current_y < dimy and current_x < dimx and current_y >= 0 and current_x >= 0:
        print("loop run")
        stream_img.putpixel((current_x, current_y), (r, g, b))
        delta_x, delta_y = random.choice(stream_deltas)
        print(f"{delta_x}, {delta_y}")
        current_x += delta_x
        current_y += delta_y
    return stream_img


if __name__ == "__main__":
    dimx, dimy = 300, 300
    img = Image.new('RGB', (dimx, dimy), (0, 0, 0))
    for i in range(0, dimx, 6):
        img = draw_stream(img, i, 0, dimx, dimy, random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
    img.show()

