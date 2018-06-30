import numpy as np
import cv2 as cv
import webcolors as wbc

def displayColour(RGB_triplet):
    pic = np.full((500,500,3), RGB_triplet[::-1], dtype=np.uint8)
    cv.imshow('ColourPic', pic)
    cv.waitKey(0)
    cv.destroyAllWindows()

# must be run in terminal for raw_input() functionality
def trainCSS3ColoursDict():
    c_dict = {}
    for key, name in wbc.css3_hex_to_names.items():
        rgb_key = wbc.hex_to_rgb(key)
        displayColour(rgb_key)
        print rgb_key, name
        new_name = raw_input('Rename as: ')
        c_dict[name] = new_name
    return c_dict

def getColourNameHTML4(rgb_triplet):
    min_colours = {}

    for key, name in wbc.html4_hex_to_names.items():
        print key, name
        r_c, g_c, b_c = wbc.hex_to_rgb(key)
        rd = (r_c - rgb_triplet[0]) ** 2
        gd = (g_c - rgb_triplet[1]) ** 2
        bd = (b_c - rgb_triplet[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def trainCSS3ColoursDictManual():
    c_dict = {}

    c_dict['lawngreen'] = 'green'
    c_dict['grey'] = 'grey'
    c_dict['darkblue'] = 'dark blue'
    c_dict['moccasin'] = 'tan'
    c_dict['ivory'] = 'tan'
    c_dict['darkviolet'] = 'purple' 
    c_dict['darkgoldenrod'] = 'tan'
    c_dict['floralwhite'] = 'white'
    c_dict['darkmagenta'] = 'purple'
    c_dict['seashell'] = 'white'
    c_dict['darkorange'] = 'orange'
    c_dict['cadetblue'] = 'blue'
    c_dict['darkslategray'] = 'grey'
    c_dict['paleturquoise'] = 'aqua'
    c_dict['lightblue'] = 'light blue'
    c_dict['snow'] = 'white'
    c_dict['dodgerblue'] = 'blue'
    c_dict['black'] = 'black'
    c_dict['darkseagreen'] = 'green' 
    c_dict['aquamarine'] = 'aqua'
    c_dict['mistyrose'] = 'tan'
    c_dict['maroon'] = 'maroon'
    c_dict['cornflowerblue'] = 'blue' 
    c_dict['royalblue'] = 'blue'
    c_dict['turquoise'] = 'turquoise'
    c_dict['white'] = 'white'
    c_dict['darkturquoise'] = 'turquoise'
    c_dict['darkred'] = 'maroon'
    c_dict['violet'] = 'pink'
    c_dict['greenyellow'] = 'lime'
    c_dict['powderblue'] = 'light blue'
    c_dict['mediumslateblue'] = 'purple'
    c_dict['magenta'] = 'magenta'
    c_dict['steelblue'] = 'blue'
    c_dict['tomato'] = 'orange'
    c_dict['springgreen'] = 'lime'
    c_dict['papayawhip'] = 'tan'
    c_dict['gold'] = 'yellow'
    c_dict['mintcream'] = 'white'
    c_dict['plum'] = 'purple'
    c_dict['indianred'] = 'coral'
    c_dict['lightsalmon'] = 'coral'
    c_dict['mediumspringgreen'] = 'lime'
    c_dict['ghostwhite'] = 'ghost'
    c_dict['green'] = 'green'
    c_dict['antiquewhite'] = 'white'
    c_dict['honeydew'] = 'white'
    c_dict['silver'] = 'grey'
    c_dict['forestgreen'] = 'green'
    c_dict['chartreuse'] = 'lime'
    c_dict['mediumpurple'] = 'purple'
    c_dict['lightgoldenrodyellow'] = 'beige' 
    c_dict['cornsilk'] = 'beige'
    c_dict['sandybrown'] = 'orange'
    c_dict['olivedrab'] = 'olive'
    c_dict['darkorchid'] = 'purple'
    c_dict['oldlace'] = 'beige'
    c_dict['mediumseagreen'] = 'green'
    c_dict['thistle'] = 'pink'
    c_dict['olive'] = 'olive'
    c_dict['darkgray'] = 'grey'
    c_dict['beige'] = 'beige'
    c_dict['wheat'] = 'beige'
    c_dict['orange'] = 'orange'
    c_dict['lime'] = 'lime'
    c_dict['lightgreen'] = 'green'
    c_dict['sienna'] = 'brown'
    c_dict['saddlebrown'] = 'brown'
    c_dict['aqua'] = 'aqua'
    c_dict['indigo'] = 'purple'
    c_dict['mediumaquamarine'] = 'olive'
    c_dict['firebrick'] = 'maroon'
    c_dict['tan'] = 'tan'
    c_dict['blanchedalmond'] = 'beige'
    c_dict['blue'] = 'blue'
    c_dict['orchid'] = 'purple'
    c_dict['lemonchiffon'] = 'beige'
    c_dict['coral'] = 'coral'
    c_dict['whitesmoke'] = 'white'
    c_dict['pink'] = 'pink'
    c_dict['khaki'] = 'tan'
    c_dict['lightyellow'] = 'beige'
    c_dict['azure'] = 'white'
    c_dict['aliceblue'] = 'white'
    c_dict['goldenrod'] = 'tan'
    c_dict['mediumvioletred'] = 'purple'
    c_dict['lightsteelblue'] = 'light blue'
    c_dict['salmon'] = 'coral'
    c_dict['deeppink'] = 'pink'
    c_dict['slateblue'] = 'purple'
    c_dict['seagreen'] = 'green'
    c_dict['darksalmon'] = 'coral'
    c_dict['lightslategrey'] = 'grey'
    c_dict['mediumorchid'] = 'purple'
    c_dict['orangered'] = 'orange'
    c_dict['brown'] = 'brown'
    c_dict['dimgrey'] = 'grey'
    c_dict['midnightblue'] = 'dark blue'
    c_dict['crimson'] = 'crimson'
    c_dict['darkkhaki'] = 'tan'
    c_dict['yellow'] = 'yellow'
    c_dict['darkolivegreen'] = 'olive'
    c_dict['palegoldenrod'] = 'beige'
    c_dict['peru'] = 'brown'
    c_dict['linen'] = 'white'
    c_dict['peachpuff'] = 'peach'
    c_dict['chocolate'] = 'brown'
    c_dict['teal'] = 'teal'
    c_dict['palegreen'] = 'lime'
    c_dict['hotpink'] = 'pink'
    c_dict['lightcyan'] = 'light blue'
    c_dict['lightskyblue'] = 'light blue'
    c_dict['navajowhite'] = 'beige'
    c_dict['darkslateblue'] = 'purple'
    c_dict['limegreen'] = 'lime'
    c_dict['lavender'] = 'pink'
    c_dict['purple'] = 'purple'
    c_dict['lightgray'] = 'grey'
    c_dict['darkgreen'] = 'olive'
    c_dict['mediumblue'] = 'blue'
    c_dict['deepskyblue'] = 'blue'
    c_dict['bisque'] = 'beige'
    c_dict['mediumturquoise'] = 'turquoise'
    c_dict['darkcyan'] = 'turquoise'
    c_dict['yellowgreen'] = 'lime'
    c_dict['lightcoral'] = 'coral'
    c_dict['red'] = 'red'
    c_dict['rosybrown'] = 'brown' 
    c_dict['palevioletred'] = 'pink'
    c_dict['lightpink'] = 'pink'
    c_dict['lightseagreen'] = 'turquoise'
    c_dict['skyblue'] = 'light blue'
    c_dict['lavenderblush'] = 'white'
    c_dict['blueviolet'] = 'purple'
    c_dict['navy'] = 'dark blue'
    c_dict['gainsboro'] = 'light grey'
    c_dict['burlywood'] = 'tan'

    return c_dict

colour_dict = trainCSS3ColoursDictManual()
np.save('colour_dict.npy', colour_dict)

# colour_dict_2 = np.load('colour_dict.npy').item()    
# print colour_dict_2['darkslategray']