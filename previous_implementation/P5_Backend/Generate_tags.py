import cv2
import numpy as np
from PIL import Image, ImageTk

#-------------------------------------------------------------------------------------------#
#DEFINES

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'



#Image Dimensions 
image_width = 400
image_height = 500
image_size = image_height*image_width #Size of training images
svm_directory = "Resources/svms/"
clasifiers = ["dress_shirt","coat"]


#SVM directory
svm_directory = "resources/svms/"

words = []

#-------------------------------------------------------------------------------------------#
def get_tags(img_array):
	#-------------------------------------------------------------------------------------------#
	#TEST SVMS FOR EACH TAG
	for tag in clasifiers:

		#-------------------------------------------------------------------------------------------#
		#LOAD THE SVM FOR THE TAG
		svm = cv2.SVM()
		svm.load(svm_directory+tag+".data")

		#-------------------------------------------------------------------------------------------#
		#TEST THE TAG
		value = svm.predict(img_array)

		#-------------------------------------------------------------------------------------------#
		#IF THE TAG IS TRUE ADD IT TO THE LIST OF CLASIFIERS
		if (value == 1):
			words.append(tag)

	#-------------------------------------------------------------------------------------------#		
	#RETURN THE TAGS
	return words

