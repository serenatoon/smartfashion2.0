from amazon.api import AmazonAPI
import sys

# set encoding to utf8 to avoid UnicodeEncode errors
reload(sys)
sys.setdefaultencoding('utf8')

amazon = AmazonAPI("AKIAIQ4EUAQUFXLIBKYA", "z4REKu6NbtgRQlvJc1Dvb2EfMjx/ycfiUUMZLqAN", "mobilea0f740b-20")

products = amazon.search(Keywords="black leather jacket", SearchIndex='All')

for i, product in enumerate(products):
    print "{0}. '{1}'".format(i, product.title)
