import numpy as np
import scipy.misc
from skimage.io import imread
from skimage import novice, data

import warnings
warnings.filterwarnings("ignore")

#set filetotal = 0 if there is only one image to be processed (not looping through a number of images)
filetotal = 75
#if filetotal = 0 , change filename to the name of the image file to be processed
filename = 'leather (6)rag_sigma230-slic_sigma0.55-n_seg1800-compactness90'

fileindex = 1
while fileindex < (filetotal + 1):
	
		print("----------------------")

		#step 1: load the image
		if (filetotal != 0):
			#filename = 'leather (' + str(fileindex) + ')' +'rag_sigma230-slic_sigma0.55-n_seg1800-compactness90' 
			filename = 'misc (' + str(fileindex) + ')' +'rag_sigma230-slic_sigma0.55-n_seg1800-compactness90' 

		path = 'output/' + str(filename) + '.png'
		print('processing ' + str(filename))
		img1 = imread(path)
		img1_prop = novice.open(path)
		img1_prop.size
		img1_width = img1_prop.width
		img1_height = img1_prop.height
		x1 = (img1_width/2) - 50
		x2 = (img1_width/2) + 50
		y1 = (img1_height/2) - 50
		y2 = (img1_height/2) + 50
		cropped = img1[x1:x2,y1:y2]
		scipy.misc.imsave('cropped/cropped-' + str(filename) + '.png', cropped)	
		fileindex += 1
	
