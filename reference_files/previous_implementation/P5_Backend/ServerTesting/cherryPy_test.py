import cherrypy
import random
import string

cherrypy.config.update({'server.socket_host': '192.168.56.1',
                        'server.socket_port': 10000,})

config = {'global': 
            {'server.socket_host': '0.0.0.0'}}

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return "Hello world!"

class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return "Hello world!"

    @cherrypy.expose
    def generate(self, length=8):
        return ''.join(random.sample(string.hexdigits, int(length)))

    @cherrypy.expose
    def ping(self):
        return "ping"

if __name__ == '__main__':
    cherrypy.quickstart(StringGenerator(), config=config)