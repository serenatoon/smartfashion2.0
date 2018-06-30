# Main.py
# 
# This script runs the backend for the SmartFashion application. It is
# split into the four key sections, background removal, tagging, product 
# search, and post-search matching.
import time
import thread
import P1_helper as P1
import P2_helper as P2
import P3_helper as P3
import P4_helper as P4

import cv2 as cv

from skimage import io as skio
from amazon.api import AmazonAPI
from amazon.api import SearchException, RequestThrottled, NoMorePages
from AmazonProduct import Product as AProduct

from multiprocessing import Process
import cPickle as pickle

# TODO Make product Class

#---------------------------------------------------------#
# GLOBAL VARS
#---------------------------------------------------------#

product_details = []

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

def saveColorBandProduct(dir, product):
    banded_img = P4.appendColourBand(product.getImg(), product.getCenteralColor() , 50)
    cv.imwrite(dir + product.getName() + ".png", product.getImg())

def filterByTag(product, tags, height=500, width=400):
    #for i, p in reversed(list(enumerate(products))):
    p_img = P2.flattenAndConvert(product.getImg(), height, width)
    for classifier in tags:
        if P2.get_binary_SVM_result(classifier, p_img) == -1:
                # remove product
            print('tag filter removing product ' + product.getName())
            #del products[i]
            return 0
    return 1;

def filterProductByColorScore(product, threshold):
    #for i in reversed(range(len(products))):
        if product.getScore > threshold:
            # remove product
            print('color filter removing product %d' % (i))
            del products[i]


def processProduct(thread_name, delay, product, source_rgb, images_path, tags, height, width, images_path_final):
    #print tags
    try:
        img = skio.imread(product.large_image_url)
    except:
        print 'Image wasn\'t found'
        return
    ap = AProduct(product.title, product.list_price[0], product.detail_page_url, img)
    print ("--------------------------------------------------------")
    print ap.getName()
    print thread_name
    print ("--------------------------------------------------------")
    time.sleep(delay)

    

    img_rgb = P4.getCentralColor(ap.getImg())
    ap.setCenteralColor(img_rgb)

    saveColorBandProduct(images_path, ap)
    time.sleep(delay)

    time.sleep(delay)
    score=P4.scoreColourDiff(img_rgb, source_rgb)
    if score > 1000:
        #print('color filter removing product' + ap.getName())
        return

    time.sleep(delay)
    ap.setScore(score)

    time.sleep(delay)
    if (filterByTag(ap, tags, height, width) == 0):
        return

    saveColorBandProduct(images_path_final, ap)

    return

#---------------------------------------------------------#
# SCRIPT PARAMETERS
#---------------------------------------------------------#

# n = 50
height = 500 
width = 400
product_images_dir = 'search_results_threaded/'
final_results_dir = 'final_results_threaded/'
amazonAcc = AmazonAPI("AKIAIQHZQNOB4KKTCJNQ", "ICQ5f+yLgk9lm/IUZODVsoCO7B0oXRZh5v8KBZDP", "ifashion08-20")


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

# performs amazon search using product advertising APIs
#product_generator = P3.yieldAmazonProducts(keywords, gender='men')

start = time.time()

# retrieve products
try:
    products = amazonAcc.search(Keywords=keywords, SearchIndex='Fashion')
    # for p in products:
    #     yield p
except:
    pass
    print "Error in Search"

P4.empty_directory(product_images_dir)    

for p in products:
    try:
        #p = AProduct(p.title, p.list_price[0], p.detail_page_url, img)
        thread.start_new_thread(processProduct, (p.title, 0.07, p, avg_color_source, product_images_dir, tags, height, width, final_results_dir))
    except:
        print "Error: unable to start thread"


# for p in products:
#     try:
#         pro = Process(target = processProduct, args = (p.title, 0.0, p, avg_color_source, product_images_dir, tags, height, width, final_results_dir))
#         pro.start()
#         pro.join()
#     except:
#         print "Error: unable to start thread"



end = time.time()
print("SECTION R TIMMING")
print(end - start)

