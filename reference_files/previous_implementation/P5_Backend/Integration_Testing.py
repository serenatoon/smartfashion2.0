from Perform_Amazon_Search import amazonFashionSearch, getSearchImages
from Generate_tags import get_tags
from Helper_Functions import empty_directory
from Dominant_Colour_Matching import getMostFrequentBand, appendColourBand, scoreColourDiff, extractSubImage, getColourName

import numpy as np
import cv2 as cv
import os
from matplotlib import pyplot as plt
from PIL import Image, ImageTk

##########################################################################

# Script Parameters
image_width = 400
image_height = 500
image_size = image_height*image_width

no_of_images = 50

img_query_file = "001.png"
input_directory = "Query_Image/"
output_directory = "Search_Results"

convert_type = 'LA' #Input image read types 'RGBA', 'LA'

bin_count = 32

##########################################################################

# retrieve query image
img = Image.open(input_directory+img_query_file).convert(convert_type)
img_query = img.resize((image_width, image_height), Image.ANTIALIAS)

flat_img = np.ravel(np.array(img_query))

# get keywords for amazon search
print 'Getting Keywords'
tags = get_tags(np.float32(flat_img))

# get query image colour
img_query = cv.imread(os.path.join(input_directory, img_query_file))
avg_query = getMostFrequentBand(extractSubImage(img_query, 0.4, 0.4), bin_count)
print 'query img colour'
print avg_query
colour_name_query = getColourName((avg_query[2], avg_query[1], avg_query[0])).encode('utf-8')
print colour_name_query

tags.append(colour_name_query)

tags_string = ' '.join(str(tag) for tag in tags)

# delete existing search
empty_directory(output_directory)

# retrieve search results from amazon
products = amazonFashionSearch(tags_string, no_of_images, gender='male')
count = getSearchImages(products, tags, output_directory)

##########################################################################

# read in images
results = []
for img_file in os.listdir(output_directory)[:count]:
    results.append(cv.imread(os.path.join(output_directory, img_file)))


##########################################################################

avg_lst = []
colour_scores = []
for i in range(len(results)):
    avg = getMostFrequentBand(extractSubImage(results[i], 0.4, 0.4), bin_count)
    avg_lst.append(avg)
    colour_scores.append(scoreColourDiff(avg, avg_query))

# print 'average colours of results'
# for j, avg_values in enumerate(avg_lst):
#     print('#%d has R:%d, G:%d, B:%d' % (j+1, avg_values[2], avg_values[1], avg_values[0]))

# print 'colour scores'
# for k, score_c in enumerate(colour_scores):
#     print('#%d has error %d' % (k+1, score_c))

# rank the products into a sorted list
ranked_results = sorted(((value, index) for index, value in enumerate(colour_scores)), reverse=False)

for value, index in ranked_results[:5]:
    print('Result no.%d has error %d' % (index+1, value))

##########################################################################

# display plot
fig, ax = plt.subplots(1, 10, subplot_kw={'adjustable': 'box-forced'})

for i in range(0, 10):
    ax[i].imshow(results[ranked_results[i][1]][:,:,::-1])
    ax[i].set_title("#%d, %d.png" % ((i+1), ranked_results[i][1]+1))

for a in ax.ravel():
    a.set_axis_off()

plt.show()