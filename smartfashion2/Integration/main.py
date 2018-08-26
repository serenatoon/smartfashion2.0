from extract_sub_image import get_sub_image
from colour_identification import identify_colour
from predict import get_prediction
from amazon_search import do_search
from slic_dir import remove_background

input_filename = 'yellowjacket.jpg'

# step 1: remove background
remove_background(input_filename)
# output will be saved to removed_bg.png

# step 2: extract sub-image
sub_img = get_sub_image('removed_bg.png')

# step 3: identify colour
#colour = identify_colour('sharpened.png')
colour = identify_colour('removed_bg.png')
#colour = identify_colour('cropped.png')
print colour

#step 4: get material
material = get_prediction('cropped.png', "material")
print material

# step 5: get type of clothing
clothing_type = get_prediction('removed_bg.png', "clothing_type")
print clothing_type

# step 6: web search
query = colour + " " + material + " " + clothing_type
print query
do_search(query)
