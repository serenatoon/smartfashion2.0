# This script extracts a 200x200pixels sub-image for 
# material detection and colour identification purposes.
# Author: Serena Toon (stoo718@aucklanduni.ac.nz)

from PIL import Image
import numpy as np
import cv2

# get 200x200 sub-image, slightly off-center
def get_sub_image(filename):
	img = Image.open(filename)
	area = (100, 300, 300, 500)
	sub_img = img.crop(area).save('cropped.png')
	sharpen()
	return sub_img


# https://www.cc.gatech.edu/classes/AY2015/cs4475_summer/documents/sharpen.py
def sharpen():
	# load image
	img = cv2.imread('cropped.png')

	#create identity filter, with 1 shifted to the right
	kernel = np.zeros((9,9), np.float32)
	kernel[4,4] = 2.0 # multiply identity by 2

	# create box filter
	box_filter = np.ones( (9,9), np.float32) / 81.0

	#subtract the two
	kernel = kernel - box_filter

	sharpened = cv2.filter2D(img, -1, kernel)
	cv2.imwrite('sharpened.png', sharpened)


#get_sub_image("removedbg.png")