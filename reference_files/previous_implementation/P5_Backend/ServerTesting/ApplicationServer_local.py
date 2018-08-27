from PIL import Image
import numpy as np
import cherrypy
import random
import string
import json
import subprocess
import hashlib
import time
import os
import sys
import thread
import base64
import io
import socket
import matplotlib.image as mpimg
import cv2 as cv
import P1_helper as P1
import P2_helper as P2
import P3_helper as P3
import P4_helper as P4        

listen_ip = "0.0.0.0"
listen_port = 13000


cherrypy.config.update({'server.socket_host': '192.168.56.1',
                        'server.socket_port': 12000,})

config = {'global': {'server.socket_host': '0.0.0.0'}}



class ApplicationServer(object):

    #---------------------------------------------------------#
    # CLASS PARAMETERS
    #---------------------------------------------------------#

    global_password = "nadeem"
    test_image = "001.jpg"
    log_path = '/logs/'
    image_path = '/test_images/'

    path = 'smartFashion'
    svm_directory = "/resources/svms/"
    results_directory = "/results/"
    final_results_dir =  "final_results/"
    product_images_dir = "search_results/"

    svm_path = path+svm_directory
    final_results_path =  path+results_directory+final_results_dir
    product_images_path = path+results_directory+product_images_dir


    n = 20
    height = 500 
    width = 400

    # prods_img = []
    # prods_images = []
    # prods_titles = []
    # prods_prices = []
    # prods_pgUrls= []
    product_details = []


    if path not in sys.path:
       sys.path.insert(0, path)

    device_dictionary = dict()  

    #---------------------------------------------------------#
    # HELPER
    #---------------------------------------------------------#

    def saveColourBandResults(self, dir, product_det, rgb_color):
        P4.empty_directory(dir)
        imgs = []
        for i in range(len(product_det)):
            banded_img = P4.appendColourBand(product_det[i].getImg(), rgb_color[i], 50)
            imgs.append(banded_img)
        P3.saveImages(imgs, dir) 

    #---------------------------------------------------------#
    # MAIN
    #---------------------------------------------------------#

    def main_process(self, thread_name, delay, image_array, gender):
        #---------------------------------------------------------#
        # MOBILE APPLICATION INTERFACE
        #---------------------------------------------------------#
        img_path = self.path+self.image_path+thread_name+"_new.png"
        
        #time.sleep(delay)
        fh = open(img_path, 'w')
        fh.write(image_array.decode('base64'))
        fh.close()
        time.sleep(delay)

        #---------------------------------------------------------#
        # BACKGROUND REMOVAL
        #---------------------------------------------------------#
        print '------------------------ Section A ------------------------'

        img_source = P1.readImageCvRGB(img_path)
        img_source_fgd = P1.removeBackgroundGrabCut(img_source)
        avg_color_source = P4.getCentralColor(img_source_fgd)
        img_source_color = P4.getColourName(avg_color_source)

        print avg_color_source
        print img_source_color
        
        time.sleep(delay)
        cv.imwrite( self.path+self.image_path+thread_name+"_backgroundRemoved.png", img_source_fgd);

        # #---------------------------------------------------------#
        # # TAGGING
        # #---------------------------------------------------------#

        print '------------------------ Section B ------------------------'

        img_source_LA = P2.flattenAndConvert(img_source_fgd, self.height, self.width)

        

        tags = P2.get_tags(img_source_LA, self.svm_path)

        keywords = tags[:]
        keywords.append(img_source_color)
        keywords = " ".join(keywords)

        print keywords

        # #---------------------------------------------------------#
        # # PRODUCT SEARCH
        # #---------------------------------------------------------#
        
        print '------------------------ Section C ------------------------'

        # performs amazon search using product advertising APIs
        product_generator = P3.yieldAmazonProducts(keywords, gender='men')

        # retrieve product details
        # each element in list is a list of product details
        # [n][0] - title
        # [n][1] - price
        # [n][2] - img
        # [n][3] - pg_url
        # <[n][4] - colourScore (added in P4)>
        self.product_details = P3.getAProductParameters(product_generator)

        print str(len(self.product_details)) + " products were found"

        # #---------------------------------------------------------#
        # # POST-SEARCH COMPARISON
        # #---------------------------------------------------------#
        print '------------------------ Section D ------------------------'

        product_images = []

        product_images[:] = [item.getImg() for item in self.product_details]

        product_img_colors, product_img_scores = P4.getColorScoresFromProduct(product_images, avg_color_source)

        # product_details = [product_details[i]+[product_img_scores[i]]+[product_img_colors[i]] for i in range(len(product_details))]

        # saving results for viewing results
        self.saveColourBandResults(self.product_images_path, self.product_details, product_img_colors)

        P4.filterByTags(self.product_details, tags, self.height, self.width)
        print str(len(self.product_details)) + " products after tag filter"

        P4.filterByColorScore(self.product_details, product_img_scores, 1000)
        print str(len(self.product_details)) + " products after color filter"

        # for i, d in enumerate(product_details):
        #     print i, d[1]

        P4.filterByPrice(self.product_details, 50)
        print str(len(self.product_details)) + " products after price filter"

        self.saveColourBandResults(self.final_results_path, self.product_details, product_img_colors)

        self.device_dictionary[thread_name] = "complete"



    @cherrypy.expose
    def index(self):
        return "Under Construction: This is the Future Website of SmartFashion"

    @cherrypy.expose
    def generate(self, length=8):
        return ''.join(random.sample(string.hexdigits, int(length)))

    def generateString(self, length=8):
        return ''.join(random.sample(string.hexdigits, int(length)))

    @cherrypy.expose
    def ping(self):
        return "ping local"

    @cherrypy.expose
    def randomJson(self):
		random_string= self.generateString()
		output_dict = {"random_string": random_string}
		data = json.dumps(output_dict)
		return data

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def passwordTest(self):
        input_data = cherrypy.request.json
        try:
            password = input_data["password"]
        except KeyError:
            output_dict = {"password_accepted": "key error"}
            data = json.dumps(output_dict)
            return data

        #Check Password
        if (password == self.global_password):
            output_dict = {"password_accepted": "true"}
        else:
            output_dict = {"password_accepted": "false"}
        data = json.dumps(output_dict)
        return data


    @cherrypy.expose
    @cherrypy.tools.json_in()
    def startQuery(self):
        input_data = cherrypy.request.json
        try:
            device_ID = input_data["device_ID"]
            password = input_data["password"]
            image_array = input_data["image_array"]
            gender = input_data["gender"]
        except KeyError:
            output_dict = {"status": "key error"}
            data = json.dumps(output_dict)
            yield data

        #Check Password
        if (password != self.global_password):
            output_dict = {"status": "password not accepted"}    
            data = json.dumps(output_dict)
            yield data

        #Check if Device ID is in the Map of devices
        if (self.device_dictionary.has_key(device_ID) == False):
            #If not then add it and update the status to accepted
            self.device_dictionary[device_ID] = "accepted"
        else:
            #Else we want to check if a query is running and terminate it before starting a new one
            if (self.device_dictionary.get(device_ID) != "finished" ):

                #Terminate the operation
                
                #Update the status to accepted        
                self.device_dictionary[device_ID] = "accepted"
                    
        self.device_dictionary[device_ID] = "accepted"        
        
        #Log request
        log_string = str(time.time())+": Start Query"
        self.log(device_ID, log_string)

        #Return status
        output_dict = {"status": self.device_dictionary.get(device_ID)}
        data = json.dumps(output_dict)
        yield data

        #Start the operation
        #thread.start_new_thread(self.main_process, (device_ID, 0.1, image_array, gender))
        self.main_process(device_ID, 0.1, image_array, gender)


    @cherrypy.expose
    @cherrypy.tools.json_in()
    def closeQuery(self):
        input_data = cherrypy.request.json
        try:
            device_ID = input_data["device_ID"]
            password = input_data["password"]
        except KeyError:
            output_dict = {"status": "key error"}
            data = json.dumps(output_dict)
            return data

        #Check Password
        if (password != self.global_password):
            output_dict = {"status": "password not accepted"}
            data = json.dumps(output_dict)
            return data    

        #Check if Device ID is in the Map of devices
        if (self.device_dictionary.has_key(device_ID)):
            #terminate query
        
            #setStatus to finished
            self.device_dictionary[device_ID] = "closed"

            #return status
            output_dict = {"status": self.device_dictionary.get(device_ID)}
            data = json.dumps(output_dict)
            return data
        else:
            #If not return an error 
            output_dict = {"status": "Query error close"}
            data = json.dumps(output_dict)
            return data

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def getStatusUpdate(self):
        input_data = cherrypy.request.json
        try:
            device_ID = input_data["device_ID"]
            password = input_data["password"]
        except KeyError:
            output_dict = {"status": "key error"}
            data = json.dumps(output_dict)
            return data
        
        #Check Password
        if (password != self.global_password):
            output_dict = {"status": "password not accepted"}    

        #Check if Device ID is in the Map of devices
        if (self.device_dictionary.has_key(device_ID)):
            #If it is return the status
            output_dict = {"status": self.device_dictionary.get(device_ID)}
            data = json.dumps(output_dict)
            return data
        else:
            #If not return an error 
            output_dict = {"status": "Query error"}
            data = json.dumps(output_dict)
            return data

        #Log request
        log_string = str(time.time())+": Get Status Update"
        self.log(device_ID, log_string)  

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def getResult(self):
        input_data = cherrypy.request.json
        try:
            device_ID = input_data["device_ID"]
            password = input_data["password"]
            result_no = input_data["result_no"]
        except KeyError:
            output_dict = {"status": "key error"}
            data = json.dumps(output_dict)
            return data

        #Check Password
        if (password != self.global_password):
            output_dict = {"status": "password not accepted"}   



        

        #Check if Device ID is in the Map of devices
        if (self.device_dictionary.has_key(device_ID)):
            #Tests
            # print ("Images Size:" + str(len(self.prods_img)))
            # print ("Titles Size:" + str(len(self.prods_titles)))
            # print ("Prices Size:" + str(len(self.prods_prices)))
            # print ("URLs Size:" + str(len(self.prods_pgUrls)))
            


            #read result
            index = int(result_no)
            #index = 3
            print ("Index: "+str(index))

            #result_image = base64.b64encode(self.prods_images[index])
            # result_image = encoded_image
            # result_url = str(self.prods_pgUrls[index])
            # result_price = str(self.prods_prices[index])
            # result_name = str(self.prods_titles[index])
            
            #save Indexed image
            #cv.imwrite( self.path+self.image_path+device_ID+"_sendImage.png", self.product_details[index].getImg());    

            #open image fle 
            #open_path =self.path+self.image_path+device_ID+"_sendImage.png"
            open_path = self.final_results_path+str(index)+".png"
            with open(open_path, "rb") as image_file:
                send_img = base64.b64encode(image_file.read())   


            #return data
            output_dict = {"status": self.device_dictionary.get(device_ID)}
            output_dict["name"] = self.product_details[index].getName()
            output_dict["image"] = send_img
            output_dict["price"] = str(self.product_details[index].getPrice())
            output_dict["url"] = self.product_details[index].getUrl() 
            data = json.dumps(output_dict)
            return data
        else:
            #If not return an error 
            output_dict = {"status": "Query error getResult"}
            data = json.dumps(output_dict)
            return data


    @cherrypy.expose
    @cherrypy.tools.json_in()
    def getImage(self):
        input_data = cherrypy.request.json
        try:
            device_ID = input_data["device_ID"]
            password = input_data["password"]
        except KeyError:
            output_dict = {"status": "key error"}
            data = json.dumps(output_dict)
            return data

        #Check Password
        if (password != self.global_password):
            output_dict = {"status": "password not accepted"}  

        #open image fle 
        open_path =self.path+self.image_path+self.test_image
        with open(open_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read())

        #return data
        output_dict = {"status": "image returned"}
        output_dict["image"] = encoded_image
        data = json.dumps(output_dict)
        return data



    @cherrypy.expose
    @cherrypy.tools.json_in()
    def setImage(self):
        input_data = cherrypy.request.json
        try:
            device_ID = input_data["device_ID"]
            password = input_data["password"]
            image_array = input_data["image_array"]
            image_height = input_data["image_height"]
            image_width = input_data["image_width"]
        except KeyError:
            output_dict = {"status": "key error"}
            data = json.dumps(output_dict)
            return data

        #Check Password
        if (password != self.global_password):
            output_dict = {"status": "password not accepted"}

        #Log request
        log_string = str(time.time())+": Get Status Update"
        self.log(device_ID, log_string)      

        #Write image
        # convert = lambda string: [int(string[i:i+2],base=16) for i in (1,3,5)]
        # B = numpy.array([map(convert,line) for line in image_array], dtype=numpy.uint8)
        # array_2 = image_array.copy()
        # image = Image.fromarray(array_2, mode="RGBA")
        # image.save(self.path+self.image_path+device_ID+".png")   
        
        fh = open(self.path+self.image_path+device_ID+".png", 'w')
        fh.write(image_array.decode('base64'))
        fh.close()

        output_dict = {"status": "accepted"}
        data = json.dumps(output_dict)
        return data

    def log(self, device_ID, log_string):
        if os.path.exists(self.path+self.log_path+device_ID):
            append_write = 'a' # append if already exists
        else:
            append_write = 'w' # make a new file if not
        
        file = open(self.path+self.log_path+device_ID,append_write)
        file.write(log_string+'\n')
        file.close()

# if __name__ == '__main__':
#     cherrypy.quickstart(ApplicationServer(), config=config)
#     
#     
#     

def runMainApp():
    # Create an instance of MainApp and tell Cherrypy to send all requests under / to it. (ie all of them)

    SERVER_INSTANCE =  ApplicationServer()
    cherrypy.tree.mount(SERVER_INSTANCE, "/")

    # Tell Cherrypy to listen for connections on the configured address and port.
    cherrypy.config.update({'server.socket_host': listen_ip,
                            'server.socket_port': listen_port,
                            'engine.autoreload.on': True,

            "/images": 
            {"tools.staticdir.on": True, 
            "tools.staticdir.dir": os.path.abspath("images")}

            #"/css": 
            #{"tools.staticdir.on":True, 
            #"tools.staticdir.dir": os.path.join(file_path, "css")}
            })

    print "========================="
    print "Starting Local Application Server"
    print "SMARTFASHION "
    print "========================================"        

    print socket.gethostbyname(socket.gethostname())               
    
    # Start the web server
    cherrypy.engine.start()

    # # Subscribe to stop
    # cherrypy.engine.subscribe('exit', SERVER_INSTANCE.exit)
    #cherrypy.log.screen = None 
    

    # And stop doing anything else. Let the web server take over.
    cherrypy.engine.block()
 
#Run the function to start everything
runMainApp()