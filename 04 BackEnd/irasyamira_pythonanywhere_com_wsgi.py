from cherrypy._cpwsgi import CPWSGIApp
from cherrypy._cptree import Application
from ServerSide import ServerSide
application = CPWSGIApp(Application(ServerSide(), ''))
