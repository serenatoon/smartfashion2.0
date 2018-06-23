from extract_sub_image import get_sub_image
from colour_identification import identify_colour
from predict import get_prediction

input_filename = 'j6885a-classic-leather-jacket-blk-leather-b.jpg'

# step 1: extract sub-image
sub_img = get_sub_image(input_filename)

# step 2: identify colour
colour = identify_colour('sharpened.png')
print colour

#step 3: get material
material = get_prediction('leather.png')
print material