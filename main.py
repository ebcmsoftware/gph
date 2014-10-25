import re
import os
import json
#import gcal
import random
import urllib
import logging
import webapp2
import urllib2

import datetime
#from datetime import datetime
from google.appengine.ext import ndb
from google.appengine.api import mail
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

def name_key(name=''):
  return ndb.Key('New Project', name)

class Project(ndb.Model):
  start = ndb.DateTimeProperty()
  end = ndb.DateTimeProperty()
  name = ndb.StringProperty() 

  @classmethod
  def query_projects(self, name):
    return self.query(ancestor=name)

  @classmethod
  def all_projects(self):
    return self.query()

def email_key(email=''):
  return ndb.Key('New User', email)

class User(ndb.Model):
  name = ndb.StringProperty(default='')
  google_acct = ndb.StringProperty(default='_')
  email = ndb.StringProperty()
  free_days = ndb.StringProperty(default='0 0 0 0 0 0 0')
  text_editor = ndb.StringProperty(default='_')
  year = ndb.IntegerProperty(default=0) # 0 = freshman, ..., 4 = grad student
  sleep_hours = ndb.StringProperty(default='_')

  @classmethod
  def query_users(self, email):
    return self.query(ancestor=email)

  @classmethod
  def all_users(self):
    return self.query()

def send_email(email=None, match=None):
    if email not in ("", None) and match not in ("", None):
        mail.send_mail(sender="the gph team todo change this lol <eric.bailey@tufts.edu>",
                       to=email,
                       subject="We've found you a project match!!",
                       body=
            """weve matched u with some1

            this is their email address: %s
            """ % (match))
    

class CreateProject(webapp2.RequestHandler):
  def post(self):
    project_query = Project.query_projects(email=email_key(email))
    token = self.request.get('token')
    response = project_query.fetch(1)
    if response == []: 
        project = Project(parent=email_key(email))
        project.name = name
        project.free_days = free_days
        project.email = email
    else:
        project = response[0]
        project.free_days = free_days
    self.response.out.write("cre8 a new proj here: (todo)")
    pass
    
  def get(self):
    self.response.out.write("write a new proj here: (todo)")


class Callback(webapp2.RequestHandler):
  def get(self):
    self.response.out.write(
    '''
    <script>
token = location.hash.split('token=')[1].split('&')[0];
window.location.href = 'http://group-40.appspot.com/getcals?token='+token;
</script>
    ''')

    logging.info(self.request.get('access_token'))
    self.response.out.write(self.request.get('access_token'))
    return

    path = os.path.join(os.path.dirname(__file__), 'index.html')
    template_values = {
    }
    self.response.out.write(template.render(path, template_values))
    return

class GetCals(webapp2.RequestHandler):
  def get(self):
    token = self.request.get('token')
    self.response.out.write(token)
    timeMin = datetime.MINYEAR
    timeMax = datetime.MAXYEAR

    #data = dict([['access_token', token], ["timeMin", timeMin], ["timeMax",timeMax]])#, ["items", jsonTime(calendarIds)])
    response = urllib2.urlopen('https://www.googleapis.com/calendar/v3/users/me/calendarList?'+token)
    self.response.out.write(response.responseText)
    #(resp, content) = http.request("https://www.googleapis.com/calendar/v3/freeBusy", "POST", urlencode(json.dumps(data)))
    
    #self.response.out.write(gcal.getGoogleFreeTime(timeMin, timeMax))

class MainHandler(webapp2.RequestHandler):
  def get(self):
    # pair people with other people
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    template_values = {
    }
    self.response.out.write(template.render(path, template_values))
    return

class AddUser(webapp2.RequestHandler):
  def post(self):
    name = self.request.get('name')
    email = self.request.get('email')
    free_days = (self.request.get('free_days'))
#TODO: assert(email is valid)
    all_users = User.all_users()
    for user in all_users:
        logging.info(user.free_days)
    user_query = User.query_users(email=email_key(email))
    response = user_query.fetch(1)
    if response == []: #create a new user
        user = User(parent=email_key(email))
        user.name = name
        user.free_days = free_days
        user.email = email
    else:
        user = response[0]
        user.free_days = free_days
    logging.info(all_users)
    overlaps = []
    for u in all_users:
        if u == user:
            continue
        logging.debug(u.free_days)
        s2 = u.free_days.split(' ')
        overlap = ''
        for i, day in enumerate(free_days.split(' ')):
            if day == s2[i]: #if we found a day match
                overlap += ' 1'
            else:
                overlap += ' 0'
        overlap = overlap.strip()
        if overlap != '0 0 0 0 0 0 0':
            overlaps.append(u.email)
    self.response.out.write(overlaps) #i have the overlaps
    user.put()

app = webapp2.WSGIApplication([
    ('/getcals', GetCals),
    ('/oauth2callback', Callback),
    ('/createproject', CreateProject),
    ('/adduser', AddUser),
    ('/', MainHandler)
], debug=True)

