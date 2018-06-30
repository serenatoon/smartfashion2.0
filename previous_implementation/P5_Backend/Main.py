# Main.py
# 
# This script runs the backend for the SmartFashion application. It is
# split into the four key sections, background removal, tagging, product
# search, and post-search matching.

import time
import os

t0 = time.time()

import P1_helper as P1
import P2_helper as P2
import P3_helper as P3
import P4_helper as P4

#---------------------------------------------------------#
# GLOBAL VARS
#---------------------------------------------------------#

#---------------------------------------------------------#
# HELPER
#---------------------------------------------------------#

# gets only the details needed for SmartFashion for each product
def getProductDetails(index, product_details):
    title = product_details[index].getTitle();
    price = product_details[index].getPrice();
    img_det = product_details[index].getImg();
    pgUrl = product_details[index].getUrl();
    return (title, price, img_det, pgUrl)

# saves the product images with their colour as seen by SmartFashion appended below the image
def saveColourBandResults(dir, product_det, rgb_color):
    P4.empty_directory(dir)
    imgs = []
    for i in range(len(product_details)):
        banded_img = P4.appendColourBand(product_det[i].getImg(), rgb_color[i], 50)
        imgs.append(banded_img)
    P3.saveImages(imgs, dir)

# saves the product images
def saveProductImages(dir, product_det):
    P4.empty_directory(dir)
    imgs = []
    for i in range(len(product_details)):
        imgs.append(product_det[i].getImg())
    P3.saveImages(imgs, dir)

#---------------------------------------------------------#
# SCRIPT PARAMETERS
#---------------------------------------------------------#

# n = 50
height = 500 
width = 400
product_images_dir = 'search_results/'
if not os.path.exists(product_images_dir):
    os.makedirs(product_images_dir)
final_results_dir = 'final_results/'
if not os.path.exists(final_results_dir):
    os.makedirs(final_results_dir)

#---------------------------------------------------------#
# MOBILE APPLICATION INTERFACE
#---------------------------------------------------------#

# receive image from mobile application

#---------------------------------------------------------#
# BACKGROUND REMOVAL
#---------------------------------------------------------#
print '#----------Background Removal----------#'
t1 = time.time()

# Query Image Path to substitute camera
path = "testcropped.jpg"

img_source = P1.readImageCvRGB(path)

# P1.displayImages([img_source, P4.extractSubImage(img_source, 0.6, 0.6)])

img_source_fgd = P1.removeBackgroundGrabCut(img_source)

# get a RGB value for the colour
avg_color_source = P4.getCentralColor(img_source_fgd)

# get a textual representation of the colour
img_source_color = P4.getColourName(avg_color_source)

print "avg colour src:", avg_color_source
print img_source_color

# P1.displayImages([img_source, img_source_fgd, P4.appendColourBand(img_source_fgd, avg_color_source, 50)])

#---------------------------------------------------------#
# TAGGING
#---------------------------------------------------------#
print '#----------Classification----------#'
t2 = time.time()

# resize image for SVM
img_source_LA = P2.flattenAndConvert(img_source_fgd, height, width)

tags = P2.get_tags(img_source_LA)

# convert tags into single string
keywords = tags[:]
keywords.append(img_source_color)
keywords = " ".join(keywords)

#---------------------------------------------------------#
# PRODUCT SEARCH
#---------------------------------------------------------#

print '#----------Web Search----------#'
t3 = time.time()

# performs amazon search using product advertising APIs
product_generator = P3.yieldAmazonProducts(keywords, gender='men')

# retrieve product details
# each element in list is a list of product details
# [n][0] - title
# [n][1] - price
# [n][2] - img
# [n][3] - pg_url
# <[n][4] - colourScore (added in P4)>
t4 = time.time()

product_details = P3.getAProductParameters(product_generator)

print str(len(product_details)) + " products were found"

#---------------------------------------------------------#
# POST-SEARCH COMPARISON
#---------------------------------------------------------#

print '#----------Post Search Scoring----------#'


product_images = []

product_images[:] = [item.getImg() for item in product_details]

# gets scores based on the colour similarity between products
product_img_colors, product_img_scores = P4.getColorScoresFromProduct(product_images, avg_color_source)

# product_details = [product_details[i]+[product_img_scores[i]]+[product_img_colors[i]] for i in range(len(product_details))]

# saving results for viewing results
saveColourBandResults(product_images_dir, product_details, product_img_colors)

P4.filterByTags(product_details, tags, product_img_colors, product_img_scores, height, width)
print str(len(product_details)) + " products after tag filter"

# P4.filterByColorScore(product_details, 1000, product_img_colors, product_img_scores)
# print str(len(product_details)) + " products after color filter"

# for i, d in enumerate(product_details):
#     print i, d[1]

# P4.filterByPrice(product_details, 20, product_img_colors, product_img_scores)
# print str(len(product_details)) + " products after price filter"=

saveColourBandResults(final_results_dir, product_details, product_img_colors)

t5 = time.time()

print("Initiaisation took %f" % (t1-t0))
print("Pre-processin took %f" % (t2-t1))
print("Tagging took %f" % (t3-t2))
print("Amazon Search took %f" % (t4-t3))
print("Post-processing took %f" % (t5-t4))