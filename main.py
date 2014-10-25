import re
import os
import json
import random
import urllib
import logging
import webapp2
import urllib2

from datetime import datetime
from google.appengine.ext import ndb
from google.appengine.api import mail
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class Project(ndb.Model):
  start = ndb.DateTimeProperty()
  end = ndb.DateTimeProperty()

class User(ndb.Model):
  name = ndb.StringProperty(default='')
  google_acct = ndb.StringProperty(default='')
  email = ndb.StringProperty()
  text_editor = ndb.StringProperty()
  year = ndb.IntegerProperty(default=0) # 0 = freshman, ..., 4 = grad student
  sleep_hours = ndb.IntegerProperty()

  @classmethod
  def query_users(self, ancestor_key):
    return self.query(ancestor=ancestor_key)


class MainHandler(webapp2.RequestHandler):
    def send_email(self, email=None, match=None):
        if email not in ("", None) and match not in ("", None):
            mail.send_mail(sender="the gph team todo change this lol <tuftswhistling@gmail.com>",
                           to=email,
                           subject="We've found you a project match!!",
                           body=
            """weve matched u with some1

            this is their email address: %s
            """ % (match))
    

    def get(self):
        # 
        # pair people with other people
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        template_values = {
        }
        self.response.out.write(template.render(path, template_values))
        return

class AddUser(webapp2.RequestHandler):
    def post(self):
        logging.debug(self.request)
        self.response.write('ohohohohohohohoh')

app = webapp2.WSGIApplication([
    ('/adduser', AddUser),
    ('/', MainHandler)
], debug=True)

