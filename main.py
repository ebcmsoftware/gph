import webapp2

import re
import os
import json
import random
import urllib
import logging
import urllib2

from datetime import datetime
from google.appengine.ext import ndb
from google.appengine.api import mail
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class MainHandler(webapp2.RequestHandler):
    def get(self):
#
        #pair people with other people
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, {}))
        return

class AddUser(webapp2.RequestHandler):
    def post(self):
        logging.debug(self.requests)
        self.response.write('ohohohohohohohoh')

app = webapp2.WSGIApplication([
    ('/adduser', AddUser),
    ('/', MainHandler)
], debug=True)

