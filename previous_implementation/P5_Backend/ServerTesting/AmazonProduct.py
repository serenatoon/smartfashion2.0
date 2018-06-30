# This file contains the definition of the amazon search product class
import base64
from skimage import io as skio

class Product:
    def __init__(self, title, price, url, img):
        self.name = title;
        self.price = price;
        self.url = url;
        self.img = img;
        self.encodedImg = base64.b64encode(img)

    def setCenteralColor(self, color):
        self.centeralColor = color

    def getCenteralColor(self):
        return self.centeralColor

    def setScore(self, colorScore):
        self.score = colorScore

    def getScore(self):
        return self.score

    def getName(self):
        return self.name

    def getPrice(self):
        return self.price

    def getUrl(self):
        return self.url
    
    def getImg(self):
        return self.img
    
    def getEncodedImg(self):
    	return self.encodedImg