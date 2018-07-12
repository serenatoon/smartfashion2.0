#!/usr/bin/python
""" serv.py

	This program uses the CherryPy web server (from www.cherrypy.org).
"""
# Requires:  CherryPy 3.2.2  (www.cherrypy.org)
#			Python  (We use 2.7)

import cherrypy
import webbrowser
import socket
import time
from extract_sub_image import get_sub_image
from colour_identification import identify_colour
from predict import get_prediction
from amazon_search import do_search
from slic_dir import remove_background

folder = 'dataset-wild-v5'
input_filename = 'leather (30).jpg'
directory = folder + '/' + input_filename


def getIPAddress():
    try:
        IPAddress = socket.gethostbyname(socket.getfqdn())
    except:
        IPAddress = socket.gethostbyname(socket.gethostname())
    return IPAddress

# The address we listen for connections on
listen_ip = "0.0.0.0"
#listen_ip = getIPAddress()
listen_port = 1234
webbrowser.open_new('http://%s:%d/' % (listen_ip, listen_port))

def processImage():	
	global s1_time, s2_time, s3_time, s4_time, s5_time, s6_time
	
	# step 1: remove background	
	s1_start = time.clock()
	remove_background(directory)
	# output will be saved to removed_bg.png
	s1_time = time.clock() - s1_start
	
	# step 2: extract sub-image  
	s2_start = time.clock()
	sub_img = get_sub_image('removed_bg.png')
	s2_time = time.clock() - s2_start
	
	# step 3: identify colour  
	s3_start = time.clock()	
	#colour = identify_colour('sharpened.png')
	colour = identify_colour('removed_bg.png')
	#colour = identify_colour('cropped.png')
	print colour
	s3_time = time.clock() - s3_start

	# step 4: get material	
	s4_start = time.clock()	
	material = get_prediction('cropped.png', "material")
	print material
	s4_time = time.clock() - s4_start

	# step 5: get type of clothing	
	s5_start = time.clock()	
	clothing_type = get_prediction('removed_bg.png', "clothing_type")
	print clothing_type
	s5_time = time.clock() - s5_start
	
	# step 6: web search  
	s6_start = time.clock()		
	query = colour + " " + material + " " + clothing_type
	print query
	do_search(query)
	s6_time = time.clock() - s6_start

class MainApp(object):

	#CherryPy Configuration
	_cp_config = {'tools.encode.on': True, 
				  'tools.encode.encoding': 'utf-8',
				  'tools.sessions.on' : 'True',
				 }				 

	# If they try somewhere we don't know, catch it here and send them to the right place.
	@cherrypy.expose
	def default(self, *args, **kwargs):
		"""The default page, given when we don't recognise where the request is for."""
		Page = "I don't know where you're trying to go, so have a 404 Error."
		cherrypy.response.status = 404
		return Page
			
		
	# PAGES (which return HTML that can be viewed in browser)
	@cherrypy.expose
	def index(self):
		Page = "This is a test WebApp for SmartFashion<br/>"		
		
		try:
			total_start = time.clock()
			processImage()
			Page += "success!\n"
			Page += 'time taken for bg rmvl (s): ' + str(s1_time) + '\n'
			Page += 'time taken for sub img extraction (s): ' + str(s2_time) + '\n'
			Page += 'time taken for colour identification (s): ' + str(s3_time) + '\n'
			Page += 'time taken for material detection (s): ' + str(s4_time) + '\n'
			Page += 'time taken for clothing type detection (s): ' + str(s5_time) + '\n'
			Page += 'time taken for web search (s): ' + str(s6_time) + '\n'
			Page += 'total time taken (s): ' + str(time.clock() - total_start) + '\n'
		except KeyError: 
			Page += "fail"
		return Page
		
def runMainApp():
	# Create an instance of MainApp and tell Cherrypy to send all requests under / to it. (ie all of them)
	cherrypy.tree.mount(MainApp(), "/")

	# Tell Cherrypy to listen for connections on the configured address and port.
	cherrypy.config.update({'server.socket_host': listen_ip,
							'server.socket_port': listen_port,
							'engine.autoreload.on': True,
						   })

	print "========================================"  
	print "University of Auckland"
	print "COMPSYS700 - Research Project"
	print "========================================"					   
	
	# Start the web server
	cherrypy.engine.start()

	# And stop doing anything else. Let the web server take over.
	cherrypy.engine.block()
 
#Run the function to start everything
runMainApp()
