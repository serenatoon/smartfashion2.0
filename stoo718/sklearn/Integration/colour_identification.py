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


def get_english_name(css3_name):
    if (css3_name == "antiquewhite" or css3_name == "bisque" or css3_name == "blanchedalmond" or css3_name == "burlywood" or css3_name == "darkkhaki" or css3_name == "lemonchiffon" or css3_name == "lightgoldenrodyellow" or css3_name == "lightyellow" or css3_name == "linen" or css3_name == "moccasin" or css3_name == "navajowhite" or css3_name == "oldlace" or css3_name == "palegoldenrod" or css3_name == "papayawhip" or css3_name == "peachpuff" or css3_name == "wheat"):
        return "beige"
    elif (css3_name == "chartreuse" or css3_name == "forestgreen" or css3_name == "limegreen" or css3_name == "mediumspringgreen" or css3_name == "springgreen" or css3_name == "yellowgreen"):
        return "green"
    elif (css3_name == "azure" or css3_name == "cornsilk" or css3_name == "floralwhite" or css3_name == "ghostwhite" or css3_name == "honeydew" or css3_name == "ivory" or css3_name == "mintcream" or css3_name == "seashell" or css3_name == "snow" or css3_name == "whitesmoke"):
        return "white"
    elif (css3_name == "blueviolet" or css3_name == "darkmagenta" or css3_name == "darkslateblue" or css3_name == "darkviolet" or css3_name == "indigo" or css3_name == "lavendar" or css3_name == "lavenderblush" or css3_name == "mediumorchid" or css3_name == "mediumpurple" or css3_name == "mediumslateblue" or css3_name == "mediumvioletred" or css3_name == "darkorchid" or css3_name == "plum" or css3_name == "rebeccapurple" or css3_name == "slateblue"):
        return "purple"
    elif (css3_name == "chocss3_nameate" or css3_name == "peru" or css3_name == "saddlebrown" or css3_name == "sienna"):
        return "brown"
    elif (css3_name == "cadetblue" or css3_name == "cornflowerblue" or css3_name == "deepskyblue" or css3_name == "dodgerblue" or css3_name == "royalblue" or css3_name == "steelblue"):
        return "blue"
    elif (css3_name == "aqua" or css3_name == "cyan" or css3_name == "darkturquoise" or css3_name == "lightseagreen" or css3_name == "mediumturquoise"):
        return "turquoise"
    elif (css3_name == "coral" or css3_name == "darkorange" or css3_name == "lightsalmon" or css3_name == "orangered" or css3_name == "salmon" or css3_name == "sandybrown" or css3_name == "tomato"):
        return "orange"
    elif (css3_name == "crimson" or css3_name == "firebrick" or css3_name == "indianred"):
        return "red"
    elif (css3_name == "darkred"):
        return "maroon"
    elif (css3_name == "darkblue" or css3_name == "mediumblue" or css3_name == "midnightblue"):
        return "navy"
    elif (css3_name == "darkcyan" or css3_name == "darkgreen" or css3_name == "darkolivegreen" or css3_name == "mediumseagreen" or css3_name == "olivedrab" or css3_name == "seagreen"):
        return "dark green"
    elif (css3_name == "darkgoldenrod" or css3_name == "goldenrod"):
        return "gold"
    elif (css3_name == "darkgray" or css3_name == "darkslategray" or css3_name == "dimgray" or css3_name == "gainsboro" or css3_name == "lightgray" or css3_name == "lightslategray" or css3_name == "silver" or css3_name == "slategray"):
        return "grey"
    elif (css3_name == "darksalmon" or "lightpink" or css3_name == "mistyrose" or css3_name == "rosybrown" or css3_name == "thistle"):
        return "light pink"
    elif (css3_name == "deeppink" or css3_name == "fuchsia" or css3_name == "hotpink" or css3_name == "magenta" or css3_name == "orchid" or css3_name == "palevioletred" or css3_name == "violet"):
        return "pink"
    elif (css3_name == "darkseagreen" or css3_name == "aquamarine" or css3_name == "lightgreen" or css3_name == "mediumaquamarine" or css3_name == "palegreen"):
        return "mint"
    elif (css3_name == "gold"):
        return "yellow"
    elif (css3_name == "greenyellow" or css3_name == "lawngreen"):
        return "lime"
    elif (css3_name == "lightblue" or css3_name == "lightcyan" or css3_name == "lightskyblue" or css3_name == "lightsteelblue" or css3_name == "aliceblue" or css3_name == "paleturquoise" or css3_name == "powderblue" or css3_name == "skyblue"):
        return "light blue"
    elif (css3_name == "lightcoral"):
        return "coral"


def identify_colour(filename):
    rgb_val = average_image_colour(filename)
    print rgb_val
    css3_name = get_colour_name(rgb_val)
    colour_name = get_english_name(css3_name)
    return colour_name


if __name__ == '__main__':
    if len(sys.argv) > 1:
            rgb_val = average_image_colour(sys.argv[1])
            print rgb_val
            colour_name = get_colour_name(rgb_val)
            print colour_name
    else:
        print 'usage: colour_identification.py FILENAME'
        print 'prints the average color of the image as (R,G,B) where R,G,B are between 0 and 255.'
