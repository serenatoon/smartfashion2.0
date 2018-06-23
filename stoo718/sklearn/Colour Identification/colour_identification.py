# https://gist.github.com/olooney/1246268

from PIL import Image
import sys

def average_image_color(filename):
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


if __name__ == '__main__':
    if len(sys.argv) > 1:
            print average_image_color(sys.argv[1])
    else:
        print 'usage: colour_identification.py FILENAME'
        print 'prints the average color of the image as (R,G,B) where R,G,B are between 0 and 255.'
