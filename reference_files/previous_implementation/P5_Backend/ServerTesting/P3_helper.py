from amazon.api import AmazonAPI
from amazon.api import SearchException, RequestThrottled, NoMorePages
from AmazonProduct import Product as AProduct
import urllib
import cStringIO
import os
import shutil
import cv2 as cv
import numpy as np
from PIL import Image
from skimage import io as skio
import time

# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# https://pypi.python.org/pypi/python-amazon-simple-product-api

# Sets up my amazon account using access key, secret key, associate-id
amazonAcc = AmazonAPI("AKIAIQHZQNOB4KKTCJNQ", "ICQ5f+yLgk9lm/IUZODVsoCO7B0oXRZh5v8KBZDP", "ifashion08-20")

# uses amazon advertising product APIs to retrieve search results for a given word 
# search under the Fashion category. Note that amazon limits it's maximum number of
# results returned.
#   words - the keywords
#   dir_out - output directory
#   n - number of results (limited by amazon)
#   gender - takes string as input, "male" or "female" else defaults blank
def amazonFashionSearch(words, n = None, gender = None):
    # include gender into search
    if (gender != None):
        words += " " + gender

    print("Searching for " + words)

    # retrieve products
    if n:
        print 'limited search'
        try:
            products = amazonAcc.search_n(n, Keywords=words, SearchIndex='Fashion')
            return products
        except:
            pass
            print "Error Searching for Products"
    else:
        print 'unbound search'
        try:
            products = amazonAcc.search(Keywords=words, SearchIndex='Fashion')
            return products
        except:
            pass
            print "Error in Search"

# def removeImglessProducts(products, products_img):

# def getImageFromURL(url): # deprecated
#     try:
#         img = skio.imread(url)
#         return img
#     except:
#         return None

def getImagesFromProducts(products):
    images = []
    
    for i, p in enumerate(products):
        try:
            img = skio.imread(p.large_image_url)
            images.append((i, img))

        except:
            pass
            
    return images

def getProductDetails(products):
    # details = [(p.title, p.list_price[0], p.detail_page_url) for p in products]
    # return details[:][0], details[:][1], details[:][2]
    titles = [p.title for p in products]
    prices = [p.list_price[0] for p in products]
    pgUrls = [p.detail_page_url for p in products]
    return titles, prices, pgUrls

def saveImages(images, dir):
    for i, img in enumerate(images):
        cv.imwrite(dir + str(i) + ".png", img[:,:,::-1])

def saveSearchImages(products, words, dir_out):
    # setup directory for results
    path = dir_out

    # create a dir to store search results
    if not os.path.exists(path):
        os.makedirs(path)

    # create text file for search result details
    file = open(os.path.join(path, 'SearchDetails.txt'),"w")
    file.write("Search for: %s\n\n" % (words))

    cnt = 1
    for product in products:
        # save image
        try:
            name = format(cnt, '03')
            urllib.urlretrieve(product.large_image_url, os.path.join(path, name + ".png"))
            file.write("%d) %s\nPrice: %s\nBrand: %s\nUrl: %s\n\n" % (cnt, product.title, product.list_price, product.brand, product.detail_page_url))
            cnt += 1
        except:
            print "Image not found"

    file.close()

    return (cnt - 1)

def yieldAmazonProducts(words, gender = None):
    # include gender into search
    if (gender != None):
        words += " " + gender

    print("Searching for " + words)

    # retrieve products
    try:
        products = amazonAcc.search(Keywords=words, SearchIndex='Fashion')
        for p in products:
            yield p

    except:
        pass
        print "Error in Search"

def getProductParameters(products):
    product_list = []
    for p in products:
        try:
            img = skio.imread(p.large_image_url)
        except:
            print 'Image wasn\'t found'
            continue
        details = [p.title, p.list_price[0], img, p.detail_page_url]
        product_list.append(details)
    return product_list

def getAProductParameters(products):
    product_list = []
    for p in products:
        try:
            img = skio.imread(p.large_image_url)
        except:
            print 'Image wasn\'t found'
            continue
        ap = AProduct(p.title, p.list_price[0], p.detail_page_url, img)
        product_list.append(ap)
    return product_list


# keywords = "pink dress shirt"
# products_iter = amazonFashionSearch(keywords, n=20, gender="mens")

# product_listing = getProductParameters(products_iter)
# print 'done'

# try:
#     for i, p in enumerate(products):
#         print i
#         try:
#             print p.title
#         except UnicodeEncodeError:
#             print 'Unicode Error'
#         time.sleep(1)
# except SearchException:
#     print 'Amazon search exception'
# except RequestThrottled:
#     print '!!! REQUEST THROTTLED !!!'
# except:
#     print 'exception'
# imgs = getImagesFromProducts(products)
# imgs_only = [i[1] for i in imgs]
# saveImages(imgs_only, "Test_DressShirtPink/")