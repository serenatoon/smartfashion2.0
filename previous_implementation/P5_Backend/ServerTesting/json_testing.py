import cherrypy
import random
import string
import json

class jsonGenerator(object):
    @cherrypy.expose
    def index(self):
        return "Hello world!"

    @cherrypy.expose
    def generate(self, length=8):
        return ''.join(random.sample(string.hexdigits, int(length)))

    def generateString(self, length=8):
        return ''.join(random.sample(string.hexdigits, int(length)))

    @cherrypy.expose
    def ping(self):
        return "ping"

    @cherrypy.expose
    def randomJson():
		randomness = self.generateString()
		output_dict = {"Random String": randomness}
		data = json.dumps(output_dict)
		return data
		

