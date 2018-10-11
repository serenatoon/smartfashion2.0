# ServerSide.py handles GET requests from the client-side of the Smartfashion system and
# executes image processing, keyword extraction using machine learning and performs the 
# Amazon search using the keywords. Results from the search are then returned to the client-side.
# Authors: Ira Sukimin (isuk218@aucklanduni.ac.nz) and Serena Toon (stoo718@aucklanduni.ac.nz)

import cherrypy
import json
import base64
import datetime
from extract_sub_image import get_sub_image
from colour_identification import identify_colour
from predict import get_prediction
from amazon_search import do_search
from slic_dir import remove_background

class ServerSide(object):

    #device_id records the device making the query for logging purposes
    device_ID = ''

	#initialise dict for results to be returned to client-side
    results_dict = {
        0: "",
        1: "",
        2: "",
        3: "",
        4: ""
    }

    results_ready = False
    device_dictionary = dict()

    #mainProcess() performs preprocessing on the query image followed by keyword extraction and Amazon search
    def mainProcess(self):
        self.logTxt("mainProcess()")

        input_filename = 'img.bmp'
        # step 1: remove background
        remove_background(input_filename)

        # step 2: extract sub-image
        get_sub_image('removed_bg.png')

        # step 3: identify colour
        colour = identify_colour('cropped.png')
        self.logTxt("identified colour: " + colour)

        #step 4: get material
        material = get_prediction('sharpened.png', "material")
        self.logTxt("identified fabric: " + material)

        # step 5: get type of clothing
        clothing_type = get_prediction('removed_bg.png', "clothing_type")
        self.logTxt("identified clothing type: " + clothing_type)

        # step 6: web search
        query = colour + " " + material + " " + clothing_type
        self.logTxt("query keywords: " + query)
        self.results_dict = do_search(query)
        self.results_ready = True

    #index() renders the webpage of irasyamira.pythonanywhere.com
    @cherrypy.expose
    def index(self):
        return "nothing to see here"

    # startQuery() receives json from client-side and saves the content of the json into variables
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def startQuery(self):
        skip = False
        self.logTxt("startQuery()")
        input_data = cherrypy.request.json

        try:
            device_ID = input_data["device_ID"]
            password = input_data["password"]
            image_array = input_data["image_array"]
        except KeyError:
            output_dict = {"status": "key error"}
            skip = True
            data = json.dumps(output_dict)
            self.logTxt("KeyError when trying to process the json received")
            yield data

        if (skip == False):
            self.logTxt("query made by " + str(device_ID))
			
            #save image array from the json received to a file for further processing
            try:
                filename = 'img.bmp'
                img_data = base64.b64decode(image_array)
                with open(filename, 'wb') as f:
                    f.write(img_data)
                self.logTxt("image has been saved as " + str(filename))
            except KeyError:
                self.logTxt("image could not be saved")

            self.mainProcess()

    #getResult() returns json containing the image, name and price of the product from Amazon
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def getResult(self):
        self.logTxt("getResult()")
        input_data = cherrypy.request.json
        while (self.results_ready == False):
            pass # do nothing

        data = json.dumps(self.results_dict)
        return data

    #logTxt() appends to a log file used for debugging purposes (~printf)
    def logTxt(self, text):
        f = open("log.txt", "a")
        f.write("\n" + str(datetime.datetime.now()) + " " + text)