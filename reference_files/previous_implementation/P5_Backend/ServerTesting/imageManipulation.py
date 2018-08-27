import numpy as np
from PIL import Image


convert_type = "RGBA"


def getImageArray(filepath):
	#open the image file
	im1 = Image.open(filepath).convert(convert_type)

	#make the image into an array
	arr = np.array(im1)

	# make a 1-dimensional view of arr
	flat_arr = arr.ravel()
	return flat_arr

def greyScale(imageArray):
	imageArray * 

	return 


