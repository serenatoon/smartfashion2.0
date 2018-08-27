from amazon.api import AmazonAPI
import urllib, cStringIO
import cv2
import os, shutil
from PIL import Image

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
def amazonFashionSearch(words, n, gender = None):
    # include gender into search
    if (gender != None):
        words += " " + gender

    print("Searching for " + words)

    # retrieve products
    try:
        products = amazonAcc.search_n(n, Keywords=words, SearchIndex='Fashion')
    except:
        pass

    return products

def getSearchImages(products, words, dir_out):
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

# example searches
# amazonFashionSearch("trench coat grey", "TrenchCoatDir", 50, gender="male")
# amazonFashionSearch("summer dress yellow", "SummerDressDir", 50, gender="female")
# amazonFashionSearch("jeans skinny blue", "JeansDir", 50)