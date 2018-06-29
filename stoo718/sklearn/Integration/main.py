from extract_sub_image import get_sub_image
from colour_identification import identify_colour
from predict import get_prediction
from amazon_search import do_search

input_filename = 'j6885a-classic-leather-jacket-blk-leather-b.jpg'

# step 1: extract sub-image
sub_img = get_sub_image(input_filename)

# step 2: identify colour
colour = identify_colour('sharpened.png')
print colour

#step 3: get material
material = get_prediction('leather.png')
print material

# step 4: get type of clothing

# step 5: web search
query = colour + " " + material + " jacket"
print query
do_search(query)
