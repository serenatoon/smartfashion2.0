import numpy as np
import cv2 as cv
import os
from matplotlib import pyplot as plt
import sys
import webcolors as wbc

path = 'smartFashion'

if path not in sys.path:
   sys.path.insert(0, path)

#---------------------------------------------------------#

colour_dictionary = {}

#---------------------------------------------------------#

def empty_directory(directory):
    for the_file in os.listdir(directory):
        file_path = os.path.join(directory, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

# function extracts a sub image from a given image. The percentage given determines
# the size of sub image, which is taken about the center of the original image.
# prcnt_h and prcnt_w are given as decimal percentages e.g. 0.6 is 60%
def extractSubImage(image, prcnt_h, prcnt_w):
    height = image.shape[0]
    width = image.shape[1]

    subimage = image[np.int(0.5*height*(1-prcnt_h)) : np.int(0.5*height*(1+prcnt_h)),
                    np.int(0.5*width*(1-prcnt_w)) : np.int(0.5*width*(1+prcnt_w)), :]

    return subimage

# function finds the average colour from all the pixels. Note that this function
# incorporates the background colour into calculation so can be very inaccurate
# returns the average RGB values as a list
def getAverageColour(image):
    pixel_cnt = image.shape[0]*image.shape[1]

    sum = [np.sum(image[:,:,0]), np.sum(image[:,:,1]), np.sum(image[:,:,2])]
    avg = [s/pixel_cnt for s in sum]

    return avg

# function finds the most common R, G, and B values from all the pixels.
def getMostFrequentColour(image):
    most_freq = []
    for i in range(0,3):
        bins = np.bincount(np.ravel(image[:,:,i]))
        most_freq.append(np.argmax(bins))

    return most_freq

# function is similar to getMostFrequentColour but finds the most freqeunt set of
# pixel RGB colours. This is more accurate, as does not confuse different colours
# with repeated R, G, or B values. But it is more computationally expensive
def getMostFrequentPixelColour(image):
    R = np.ravel(image[:,:,0])

    G = np.ravel(image[:,:,1])
    left_8 = np.full_like(G, 8)
    G = np.left_shift(G, left_8, dtype=np.uint16)

    B = np.ravel(image[:,:,2])
    left_16 = np.full_like(B,16)
    B = np.left_shift(B, left_16, dtype=np.uint32)
 
    RGB_array = np.bitwise_or(np.bitwise_or(R, G), B)
    most_freq_pixel = np.bincount(RGB_array).argmax()  

    most_freq_R = most_freq_pixel & 255
    most_freq_pixel = most_freq_pixel >> 8

    most_freq_G = most_freq_pixel & 255
    most_freq_B = most_freq_pixel >> 8

    return [most_freq_R, most_freq_G, most_freq_B]

def getMostFrequentBand(image, bin_cnt):
    R = np.ravel(image[:,:,0])
    G = np.ravel(image[:,:,1])
    B = np.ravel(image[:,:,2])

    R_hist, R_edges = np.histogram(R, bins=bin_cnt, range=(0,256))
    G_hist, G_edges = np.histogram(G, bins=bin_cnt, range=(0,256))
    B_hist, B_edges = np.histogram(B, bins=bin_cnt, range=(0,256))

    R_ind = np.argmax(R_hist)
    G_ind = np.argmax(G_hist)
    B_ind = np.argmax(B_hist)

    R_freq = (R_edges[R_ind] + R_edges[R_ind+1])/2
    G_freq = (R_edges[G_ind] + R_edges[G_ind+1])/2
    B_freq = (R_edges[B_ind] + R_edges[B_ind+1])/2


    return [R_freq, G_freq, B_freq]

def getCentralColor(image):
    subImg = extractSubImage(image, 0.4, 0.4)
    rgb_val = getMostFrequentBand(subImg, 32)
    return rgb_val

def getColorScoresFromProduct(images, source_rgb):
    colors = []
    scores = []
    for i in range(len(images)):
        img_rgb = getCentralColor(images[i])
        colors.append(img_rgb)
        scores.append(scoreColourDiff(img_rgb, source_rgb))

    return colors, scores

# function appends colour band to bottom of image
# colour band is represented as a 3 element list of the uint8 RGB values
def appendColourBand(image, band, height):
    dominant_colour = np.empty((height, image.shape[1], 3), dtype=np.uint8)
    
    for i in range(0,3):
        dominant_colour[:,:,i] = np.full((height, image.shape[1]), band[i], dtype=np.uint8)
    
    image = np.concatenate((image, dominant_colour), axis=0)

    return image

# function returns a score based on the mean squared error between the avg RGB values
# for two images
def scoreColourDiff(avg1, avg2):
    sqm_error = 0
    for i in range(len(avg1)):
        sqm_error += (avg1[i] - avg2[i]) ** 2
    return sqm_error

# function finds names RGB values with their closest name under CSS 3 then
# converts it to its closest common colour name
# https://stackoverflow.com/questions/9694165/convert-rgb-color-to-english-color-name-like-green
def getColourName(rgb_triplet):
    min_colours = {}
    for key, name in wbc.css3_hex_to_names.items():
        r_c, g_c, b_c = wbc.hex_to_rgb(key)
        rd = (r_c - rgb_triplet[0]) ** 2
        gd = (g_c - rgb_triplet[1]) ** 2
        bd = (b_c - rgb_triplet[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    css3_name = min_colours[min(min_colours.keys())]
    print css3_name
    return colour_dictionary[css3_name]

def loadColourDictionary():
    dict = np.load('smartFashion/colour_dict.npy').item()    
    return dict

#---------------------------------------------------------#

import P2_helper as P2

def filterByTags(products, tags, height=500, width=400):
    for i, p in reversed(list(enumerate(products))):
        p_img = P2.flattenAndConvert(p.getImg(), height, width)
        for classifier in tags:
            if P2.get_binary_SVM_result(classifier, p_img) == -1:
                # remove product
                print('tag filter removing product %d' % (i))
                del products[i]
                break

def filterByTags(products, tags, height=500, width=400):
    for i, p in reversed(list(enumerate(products))):
        p_img = P2.flattenAndConvert(p.getImg(), height, width)
        for classifier in tags:
            if P2.get_binary_SVM_result(classifier, p_img) == -1:
                # remove product
                print('tag filter removing product %d' % (i))
                del products[i]
                break

def filterByColorScore(products, scores, threshold):
    for i in reversed(range(len(products))):
        if scores[i] > threshold:
            # remove product
            print('color filter removing product %d' % (i))
            del products[i]

def filterByPrice(products, price_thresh):
    for i, p in reversed(list(enumerate(products))):
        if p.getPrice() > price_thresh:
            # remove product
            print('price filter removing product %d' % (i))
            del products[i]
    
#---------------------------------------------------------#

print 'loading colour dictionary'
colour_dictionary = loadColourDictionary()

# path = "Query_Image/002.png"
# imgCv = readImageCvRGB(path)
# imgSk = readImageSkRGB(path)

# display plot
# fig, ax = plt.subplots(1, 2, subplot_kw={'adjustable': 'box-forced'})

# ax[0].imshow(imgCv)    
# ax[0].set_title('CV')
# ax[1].imshow(imgB)    
# ax[1].set_title('Result')

# for a in ax.ravel():
#     a.set_axis_off()

# plt.show()