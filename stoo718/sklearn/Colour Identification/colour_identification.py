from PIL import Image
import sys
import webcolors

# https://gist.github.com/olooney/1246268
def average_image_colour(filename):
    i = Image.open(filename)
    h = i.histogram()

    # split into red, green, blue
    r = h[0:256]
    g = h[256:256*2]
    b = h[256*2: 256*3]

    # perform the weighted average of each channel:
    # the *index* is the channel value, and the *value* is its weight
    return (
        sum(i*w for i, w in enumerate(r)) / sum(r),
        sum(i*w for i, w in enumerate(g)) / sum(g),
        sum(i*w for i, w in enumerate(b)) / sum(b)
    )


# https://stackoverflow.com/questions/9694165/convert-rgb-color-to-english-color-name-like-green-with-python
def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]


def get_colour_name(requested_colour):
    try:
        name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        name = closest_colour(requested_colour)
    return name


if __name__ == '__main__':
    if len(sys.argv) > 1:
            rgb_val = average_image_colour(sys.argv[1])
            print rgb_val
            colour_name = get_colour_name(rgb_val)
            print colour_name
    else:
        print 'usage: colour_identification.py FILENAME'
        print 'prints the average color of the image as (R,G,B) where R,G,B are between 0 and 255.'
