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
import matplotlib.image as mpimg
from AmazonProduct import Product as AProduct
from amazon.api import AmazonAPI
from amazon.api import SearchException, RequestThrottled, NoMorePages
import cv2 as cv
from skimage import io as skio
import P1_helper as P1
import P2_helper as P2
import P3_helper as P3
import P4_helper as P4        






class ApplicationServer(object):

    #---------------------------------------------------------#
    # CLASS PARAMETERS
    #---------------------------------------------------------#

    global_password = "nadeem"
    test_image = "001.jpg"
    log_path = '/logs/'
    image_path = '/test_images/'

    path = '/home/SmartFashion/smartFashion'
    svm_directory = "/resources/svms/"
    results_directory = "/results/"
    final_results_dir =  "final_results/"
    product_images_dir = "search_results/"

    amazonAcc = AmazonAPI("AKIAIB7YUHUV766MDVRQ", "FQhfh7SInbyQARF8cmGIX0YPPAgpnFUXxxsXypay", "martashion-20 ")

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
    results_list = []


    if path not in sys.path:
       sys.path.insert(0, path)

    device_dictionary = dict()  
    cached_prods = dict()

    #---------------------------------------------------------#
    # HELPER
    #---------------------------------------------------------#
    def filterByTag(self, product, tags, height=500, width=400):
    #for i, p in reversed(list(enumerate(products))):
        p_img = P2.flattenAndConvert(product.getImg(), height, width)
        for classifier in tags:
            if P2.get_binary_SVM_result(classifier, p_img) == -1:
                    # remove product
                # print('tag filter removing product ' + product.getName())
                #del products[i]
                return 0
        return 1;

    def saveColourBandResults(self, dir, product_det, rgb_color):
        P4.empty_directory(dir)
        imgs = []
        for i in range(len(product_det)):
            banded_img = P4.appendColourBand(product_det[i].getImg(), rgb_color[i], 50)
            imgs.append(banded_img)
        P3.saveImages(imgs, dir) 

    def filterProductByColorScore(self, product, threshold):
        for i in reversed(range(len(products))):
            if product.getScore > threshold:
                # remove product
                # print('color filter removing product %d' % (i))
                del products[i]

    def saveColorBandProduct(self, dir, product):
	    banded_img = P4.appendColourBand(product.getImg(), product.getCenteralColor() , 50)
	    cv.imwrite(dir + product.getName() + ".png", banded_img[:,:,::-1])  

    def saveProduct(dir, product):
        img = product.getImg()
        cv.imwrite(dir + product.getName() + ".png", img[:,:,::-1])       

    def saveColorBandProductScore(self, dir, product):
	    banded_img = P4.appendColourBand(product.getImg(), product.getCenteralColor() , 50)
	    cv.imwrite(dir +str(product.getScore())+"_"+product.getName() + ".png", banded_img[:,:,::-1])





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

        log_string = str(time.time())+": MAIN PROCESS"
        self.log(thread_name, log_string) 


        #---------------------------------------------------------#
        # BACKGROUND REMOVAL
        #---------------------------------------------------------#
        print ('------------------------ Section A ------------------------')

        img_source = P1.readImageCvRGB(img_path)
        img_source_fgd = P1.removeBackgroundGrabCut(img_source)
        avg_color_source = P4.getCentralColor(img_source_fgd)
        img_source_color = P4.getColourName(avg_color_source)

        print (avg_color_source)
        print (img_source_color)
        
        time.sleep(delay)
        cv.imwrite( self.path+self.image_path+thread_name+"_backgroundRemoved.png", img_source_fgd);

        log_string = str(time.time())+": SECTION A COMPLETE"
        self.log(thread_name, log_string) 

        # #---------------------------------------------------------#
        # # TAGGING
        # #---------------------------------------------------------#

        print ('------------------------ Section B ------------------------')

        img_source_LA = P2.flattenAndConvert(img_source_fgd, self.height, self.width)        

        tags = P2.get_tags(img_source_LA, self.svm_path)

        keywords = tags[:]
        keywords.append(img_source_color)
        keywords = " ".join(keywords)
        keypath = gender+"_"+keywords

        print ("This is the keypath: "+keypath)

        log_string = str(time.time())+": SECTION B COMPLETE: Keypath ="+keypath
        self.log(thread_name, log_string) 

        # #---------------------------------------------------------#
        # # PRODUCT SEARCH
        # #---------------------------------------------------------#
        
        print ('------------------------ Section C ------------------------')

        # performs amazon search using product advertising APIs
        #product_generator = P3.yieldAmazonProducts(keywords, gender=gender)

        # retrieve product details
        # each element in list is a list of product details
        # [n][0] - title
        # [n][1] - price
        # [n][2] - img
        # [n][3] - pg_url
        # <[n][4] - colourScore (added in P4)>
        #self.product_details = P3.getAProductParameters(product_generator)

        #print str(len(self.product_details)) + " products were found"
        # retrieve products
        try:
        	products = self.amazonAcc.search(Keywords=keywords, SearchIndex='Fashion')
            for p in products:
                yield p
        except:
            pass
        	print "Error in search"

        self.results_list = []    

        log_string = str(time.time())+": SECTION C COMPLETE: Keypath ="
        self.log(thread_name, log_string) 
        # #---------------------------------------------------------#
        # # POST-SEARCH COMPARISON
        # #---------------------------------------------------------#
        print ('------------------------ Section D ------------------------')

        P4.empty_directory(self.product_images_path)
        P4.empty_directory(self.final_results_path)

        #create a new directory for the cached images
        cache_path = self.path+self.results_directory+keypath
        
         #Check if Device ID is in the Map of devices
        if (self.cached_prods.has_key(keypath)):
            print ("using cahcned products")
            cached_list = self.cached_prods(keypath)
            for ap in cached_list:
                self.saveColorBandProduct(self.product_images_path, ap)

                #Score the product
                score = P4.scoreColourDiff(ap.getCentralColor(), avg_color_source)
                if (self.filterByTag(ap, tags, self.height, self.width) == 0):
                    score = score + 100000
                ap.setScore(score)  

                #print "saving scored image"
                self.saveColorBandProductScore(self.final_results_path, ap)    

                self.results_list.append((score,ap))

        else:
            print ("geting new products")
            cached_list = []
            read_images = 0
            images_not_found = 0
            for p in products:
                try:
                   
                    img = skio.imread(p.large_image_url)
                    #print "read image"
                    read_images = read_images + 1

                    ap = AProduct(p.title, p.list_price[0], p.detail_page_url, img)
                    img_rgb = P4.getCentralColor(ap.getImg())
                    ap.setCenteralColor(img_rgb)

                    #save the 
                    #self.saveProduct(cache_path, ap)

                    #print "saving image"
                    self.saveColorBandProduct(self.product_images_path, ap)

                    #Score the product
                    score = P4.scoreColourDiff(img_rgb, avg_color_source)
                    if (self.filterByTag(ap, tags, self.height, self.width) == 0):
                        score = score + 100000
                    ap.setScore(score)  

                    #print "saving scored image"
                    self.saveColorBandProductScore(self.final_results_path, ap)     

                    cached_list.append(ap)
                    self.results_list.append((score,ap))

                except:
                    images_not_found = images_not_found + 1
                    #print "Image wasn't found"

            print("Images Read"+str(read_images))
            print("Images not found"+str(images_not_found)) 

            #save the cached list of prods in the dict
            self.cached_prods[keypath] = cached_list

        self.results_list.sort(key=lambda tup: tup[0])
            

        # product_images = []

        # product_images[:] = [item.getImg() for item in self.product_details]

        # product_img_colors, product_img_scores = P4.getColorScoresFromProduct(product_images, avg_color_source)

        # # saving results for viewing results
        # self.saveColourBandResults(self.product_images_path, self.product_details, product_img_colors)

        # P4.filterByTags(self.product_details, tags, product_img_colors, product_img_scores, self.height, self.width)
        # #print str(len(self.product_details)) + " products after tag filter"

        # P4.filterByColorScore(self.product_details, 1000, product_img_colors, product_img_scores)
        # #print str(len(self.product_details)) + " products after color filter"

        # # P4.filterByPrice(self.product_details, 50, product_img_colors, product_img_scores)
        # # print str(len(self.product_details)) + " products after price filter"

        # self.saveColourBandResults(self.final_results_path, self.product_details, product_img_colors)

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
        return "ping"

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

            (score, ap) = self.results_list[index]

            name = ap.getName()
            score = str(score)

            #result_image = base64.b64encode(self.prods_images[index])
            # result_image = encoded_image
            # result_url = str(self.prods_pgUrls[index])
            # result_price = str(self.prods_prices[index])
            # result_name = str(self.prods_titles[index])
            
            #save Indexed image
            #cv.imwrite( self.path+self.image_path+device_ID+"_sendImage.png", self.product_details[index].getImg());    

            #open image fle 
            #open_path =self.path+self.image_path+device_ID+"_sendImage.png"
            #open_path = self.final_results_path+str(index)+".png"
            open_path = self.final_results_path+score+"_"+name+".png"
            with open(open_path, "rb") as image_file:
                send_img = base64.b64encode(image_file.read())   


            #return data
            output_dict = {"status": self.device_dictionary.get(device_ID)}
            output_dict["name"] = name
            output_dict["image"] = send_img
            output_dict["price"] = ap.getPrice()
            output_dict["url"] = ap.getUrl() 
            data = json.dumps(output_dict)
            # output_dict["name"] = self.product_details[index].getName()
            # output_dict["image"] = send_img
            # output_dict["price"] = str(self.product_details[index].getPrice())
            # output_dict["url"] = self.product_details[index].getUrl() 
            # data = json.dumps(output_dict)
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