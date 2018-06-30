import cv2
import numpy as np
import sys
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
#svm_directory = "Resources/svms/"
classifiers = ["dress_shirt","coat"]


#SVM directory
path = 'smartFashion'
svm_directory = "/resources/svms/"
svm_path = path+svm_directory

words = []

if path not in sys.path:
   sys.path.insert(0, path)

#-------------------------------------------------------------------------------------------#
def get_tags(img_array):
	#-------------------------------------------------------------------------------------------#
	#TEST SVMS FOR EACH TAG
	for tag in classifiers:

		#-------------------------------------------------------------------------------------------#
		#LOAD THE SVM FOR THE TAG
		svm = cv2.SVM()
		#print(svm_directory+tag+".data")
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

#-------------------------------------------------------------------------------------------#
def get_tags(img_array, svm_path=svm_path):
	#-------------------------------------------------------------------------------------------#
	#TEST SVMS FOR EACH TAG
	for tag in classifiers:

		#-------------------------------------------------------------------------------------------#
		#LOAD THE SVM FOR THE TAG
		svm = cv2.SVM()
		print(svm_path+tag+".data")
		svm.load(svm_path+tag+".data")

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

def get_binary_SVM_result(tag, img_array):
    svm = cv2.SVM()
    path = svm_path+tag+".data"
    #print path
    svm.load(path)
    value = svm.predict(img_array)
    return value

def readImageLA(path):
    """
    Reads image using 
    Args:
        path: the file path of image

    Returns:
        image as numpy array 
    """
    img = open(path).convert('LA')
    return img

def flattenAndConvert(source, height, width):
    # img = array_src.resize((width, height), Image.ANTIALIAS)
    source_array = cv2.resize(source, (width, height))
    source_LA = Image.fromarray(source_array, mode='LA')
    source_flat = np.ravel(np.array(source_LA))
    return np.float32(source_flat)