from PIL import Image
import numpy as np

# get 200x200 sub-image, slightly off-center
def get_sub_image(filename):
	img = Image.open(filename)
	width, height = img.size

	top_edge = .40 * height
	left_edge = .55 * width
	area = (left_edge, top_edge, left_edge+200, top_edge+200)

	sub_img = img.crop(area).save('cropped.png')


get_sub_image("removedbg.png")