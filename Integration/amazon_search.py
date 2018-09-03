from amazon.api import AmazonAPI
import sys
import os
import urllib

# set encoding to utf8 to avoid UnicodeEncode errors
reload(sys)
sys.setdefaultencoding('utf8')

# set/create results dir
output_dir = 'final_results/'
# create dir if does not exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
else: # empty the directory if already exists
    for file in os.listdir(output_dir):
        file_path = os.path.join(output_dir, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)


amazon = AmazonAPI("AKIAIQ4EUAQUFXLIBKYA", "z4REKu6NbtgRQlvJc1Dvb2EfMjx/ycfiUUMZLqAN", "mobilea0f740b-20")


def do_search(query):
    products = amazon.search(Keywords=query, SearchIndex='All')

    for i, product in enumerate(products):
        name = "{0}. {1} ${2}".format(i, product.title, product.list_price[0])
        #print name
        price = "${0}".format(product.list_price[0])
        #print price
        results = {
            "title": "",
            "price": "",
            "img": ""
        }

        # get image
        try:
            urllib.urlretrieve(product.large_image_url, os.path.join(output_dir, name + ".png"))
            results["title"] = product.title
            results["price"] = price
            results["img"] = product.large_image_url

            print results
        except:
            print "Could not retrieve image"

#do_search("black leather jacket")