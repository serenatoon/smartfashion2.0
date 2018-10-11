# This script performs an Amazon search using keywords extracted.
# A dict containing information on the clothing item is returned.
# Author: Serena Toon (stoo718@aucklanduni.ac.nz)

from amazon.api import AmazonAPI
import sys
import os
import urllib
import datetime
import requests
import base64
import shutil

# set encoding to utf8 to avoid UnicodeEncode errors
reload(sys)
sys.setdefaultencoding('utf8')

def getb64(url):
    return base64.b64encode(requests.get(url).content)

def logTxt(text):
    f = open("log.txt", "a")
    f.write("\n" + str(datetime.datetime.now()) + " " + text)

# set/create results dir
output_dir = 'final_results/'
amazon = AmazonAPI("AKIAIQ4EUAQUFXLIBKYA", "z4REKu6NbtgRQlvJc1Dvb2EfMjx/ycfiUUMZLqAN", "mobilea0f740b-20")

def do_search(query):

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    else: # empty the directory if already exists
        shutil.rmtree(output_dir)
        os.makedirs(output_dir)

    products = amazon.search(Keywords=query, SearchIndex='All')
    results_dict = {
        0: "",
        1: "",
        2: "",
        3: "",
        4: ""
    }
    results_count = 0

    for i, product in enumerate(products):
        name = "{0}. {1} ${2}".format(i, product.title, product.list_price[0])
        #print name
        price = "{0}".format(product.list_price[0])
        #print price
        results = {
            "title": "",
            "price": "",
            "img": "",
            "url": ""
        }

        # get image
        try:
            urllib.urlretrieve(product.large_image_url, os.path.join(output_dir, name + ".png"))
            results["title"] = product.title
            results["price"] = price
            results["img"] = getb64(product.large_image_url)
            results["url"] = product.detail_page_url
            results_dict[results_count] = results
            logTxt(product.title)
            results_count += 1
            if (results_count >= 10):
                return results_dict
        except:
            if (results_count > 0):
                results_count -= 1
            logTxt("could not retrieve image for " + product.title)
            # do nothing

    return None