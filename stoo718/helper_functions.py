import os
import numpy as np
from PIL import Image, ImageTk

convert_type = 'LA' #Input image read types 'RGBA', 'LA'
ext = ".png"


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def resize(input_directory, output_directory, image_width, image_height):
    #Get images form directory
    for filename in os.listdir(input_directory):
        #print filename
        if filename.endswith(".png") or filename.endswith(".jpg"):
            filename_wo_ext = os.path.splitext(filename)[0]
            imageFile = filename


            #Open Image
            im1 = Image.open(input_directory+imageFile)

            #Use one of these filter options to resize the image
            #im2 = im1.resize((image_width, image_height), Image.NEAREST)      # use nearest neighbour
            #im3 = im1.resize((image_width, image_height), Image.BILINEAR)     # linear interpolation in a 2x2 environment
            #im4 = im1.resize((image_width, image_height), Image.BICUBIC)      # cubic spline interpolation in a 4x4 environment
            im5 = im1.resize((image_width, image_height), Image.ANTIALIAS)    # best down-sizing filter

            #Save Images
            # im2.save(filename_wo_ext+"_"+"NEAREST" + ext)
            # im3.save(filename_wo_ext+"_"+"BILINEAR" + ext)
            # im4.save(filename_wo_ext+"_"+"BICUBIC" + ext)
            im5.save(output_directory+filename_wo_ext+ext)

            im5.close()
            im1.close()

def create_matrix(positive_directory, negative_directory):
    #Get images form positive directory and create a Matrix from them
    print "SETTING UP MATRIX WITH POSITIVE IMAGES"

    #VARIABLES
    matrix = np.array
    index = 0

    for filename in os.listdir(positive_directory):
        if filename.endswith(".png") or filename.endswith(".jpg"): 
            
            img = Image.open(positive_directory+filename).convert(convert_type)
            arr = np.array(img)

            # record the original shape
            shape = arr.shape

            # make a 1-dimensional view of arr
            flat_arr = arr.ravel()

            # # convert it to a matrix
            # vector = np.matrix(flat_arr)
            if (index == 0):
                matrix = flat_arr
            else:
                matrix = np.vstack([matrix, flat_arr])
            
            img.close()
            index = index+1
            
    #Get size of training matrix with only positive images
    positive_image_no = index
    print "POSITIVE IMAGES COMPLETE, SIZE EQUALS: " + str(positive_image_no)

    #Get images form positive directory and add them to the training Matrix from them
    print "ADDING NEGATIVE IMAGES TO MATRIX"
    for filename in os.listdir(negative_directory):
        if filename.endswith(".png") or filename.endswith(".jpg"): 
            img = Image.open(negative_directory+filename).convert(convert_type)
            arr = np.array(img)

            # record the original shape
            shape = arr.shape

            # make a 1-dimensional view of arr
            flat_arr = arr.ravel()

            

            if (index == 0):
                matrix = flat_arr
            else:
                matrix = np.vstack([matrix, flat_arr])
            
            img.close()
            index = index+1


    negative_image_no = index - positive_image_no
    print "NEGATIVE IMAGES COMPLETE SIZE EQUALS: " + str(negative_image_no)

    return (matrix, positive_image_no, negative_image_no)

def percentage_match(array_A, array_B):
    #CHECK IF array_A AND PREDICTION MATRIX HAVE SAME SIZE
    if array_A.size == array_B.size : 
        print bcolors.OKGREEN + "[SUCCESS] BOTH array_A AND array_B HAVE SAME SIZE" + bcolors.ENDC
    else:
        print bcolors.WARNING + "[ERROR] BOTH array_A AND array_B HAVE DIFFERENT SIZE" + bcolors.ENDC

    match = 0
    mismatch = 0
    for i in range(0,array_A.size):
        if array_A[i] == array_B[i] :
            match =  match+1
        else: 
            mismatch = mismatch+1
        

    percentage_match_val = (float(match)/float(array_A.size))*100

    return percentage_match_val