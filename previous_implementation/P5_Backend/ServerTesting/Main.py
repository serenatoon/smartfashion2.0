# Main.py
# 
# This script runs the backend for the SmartFashion application. It is
# split into the four key sections, background removal, tagging, product 
# search, and post-search matching.
import time
import P1_helper as P1
import P2_helper as P2
import P3_helper as P3
import P4_helper as P4

# TODO Make product Class

#---------------------------------------------------------#
# GLOBAL VARS
#---------------------------------------------------------#

#---------------------------------------------------------#
# HELPER
#---------------------------------------------------------#

def getProductDetails(index, product_details):
    title = product_details[index].getTitle();
    price = product_details[index].getPrice();
    img_det = product_details[index].getImg();
    pgUrl = product_details[index].getUrl();
    return (title, price, img_det, pgUrl)

def saveColourBandResults(dir, product_det, rgb_color):
    P4.empty_directory(dir)
    imgs = []
    for i in range(len(product_details)):
        banded_img = P4.appendColourBand(product_det[i].getImg(), rgb_color[i], 50)
        imgs.append(banded_img)
    P3.saveImages(imgs, dir)


#---------------------------------------------------------#
# SCRIPT PARAMETERS
#---------------------------------------------------------#

# n = 50
height = 500 
width = 400
product_images_dir = 'search_results/'
final_results_dir = 'final_results/'

#---------------------------------------------------------#
# MOBILE APPLICATION INTERFACE
#---------------------------------------------------------#

# receive image from mobile application

#---------------------------------------------------------#
# BACKGROUND REMOVAL
#---------------------------------------------------------#
print '#----------Section A----------#'
start = time.time()




# Query Image Path to substitute camera
path = "Query_Image/005.png"

img_source = P1.readImageCvRGB(path)

img_source_fgd = P1.removeBackgroundGrabCut(img_source)

avg_color_source = P4.getCentralColor(img_source_fgd)

img_source_color = P4.getColourName(avg_color_source)

print avg_color_source
# print img_source_color

# P1.displayImages([img_source, img_source_fgd, P4.appendColourBand(img_source_fgd, avg_color_source, 50)])
end = time.time()
print("SECTION A TIMMING")
print(end - start)
#---------------------------------------------------------#
# TAGGING
#---------------------------------------------------------#
print '#----------Section B----------#'
start = time.time()
img_source_LA = P2.flattenAndConvert(img_source_fgd, height, width)

tags = P2.get_tags(img_source_LA)

keywords = tags[:]
keywords.append(img_source_color)
keywords = " ".join(keywords)

end = time.time()
print("SECTION B TIMMING")
print(end - start)
#---------------------------------------------------------#
# PRODUCT SEARCH
#---------------------------------------------------------#

print '#----------Section C----------#'
start = time.time()
# performs amazon search using product advertising APIs
product_generator = P3.yieldAmazonProducts(keywords, gender='men')

# retrieve product details
# each element in list is a list of product details
# [n][0] - title
# [n][1] - price
# [n][2] - img
# [n][3] - pg_url
# <[n][4] - colourScore (added in P4)>
product_details = P3.getAProductParameters(product_generator)

print str(len(product_details)) + " products were found"

end = time.time()
print("SECTION C TIMMING")
print(end - start)
#---------------------------------------------------------#
# POST-SEARCH COMPARISON
#---------------------------------------------------------#

print '#----------Section D----------#'
start = time.time()
product_images = []

product_images[:] = [item.getImg() for item in product_details]

product_img_colors, product_img_scores = P4.getColorScoresFromProduct(product_images, avg_color_source)

# product_details = [product_details[i]+[product_img_scores[i]]+[product_img_colors[i]] for i in range(len(product_details))]

# saving results for viewing results
saveColourBandResults(product_images_dir, product_details, product_img_colors)

P4.filterByTags(product_details, tags, height, width)
print str(len(product_details)) + " products after tag filter"

P4.filterByColorScore(product_details, product_img_scores, 1000)
print str(len(product_details)) + " products after color filter"

# for i, d in enumerate(product_details):
#     print i, d[1]

P4.filterByPrice(product_details, 20)
print str(len(product_details)) + " products after price filter"

saveColourBandResults(final_results_dir, product_details, product_img_colors)

end = time.time()
print("SECTION D TIMMING")
print(end - start)