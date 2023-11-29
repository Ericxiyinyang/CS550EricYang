from PIL import Image


def mandelbrot(c, z=complex(0,0), count=0):
	znew = z**2+c

	count += 1

	if abs(znew) >= 2 or count >= 3:
		return count
	return mandelbrot(c, znew, count)	

numescape = mandelbrot(complex(0, 1.5))
print(numescape)

dimx, dimy = 9, 9
image = Image.new("RGB", (dimx, dimy))

y = -2
yloc = 0
x = -2
xloc = 0
while y <= 2:
	while x <= 2:
		numescape = mandelbrot(complex(x, y))
		if numescape == 1:
			color = (255, 0, 0)
		elif numescape == 2:
			color = (0, 255, 0)
		else:
			color = (0, 0, 255)
		image.putpixel((xloc, yloc), color)
		x += .5
		xloc += 1
	xloc = 0
	x = -2
	yloc += 1
	y += .5

image.show()
