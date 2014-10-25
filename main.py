import re
import os
import json
#import gcal
import random
import urllib
import urllib2
import logging
import webapp2
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
  #name = ndb.StringProperty() 

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
    

class GetProject(webapp2.RequestHandler):
  def get(self):
    projects = Project.all_projects()
    response = projects.fetch(1)
    if response == []: 
        self.response.out.write('no there arent projects')
        return
    else:
        project = response[0]
    logging.info(project)
    def to_utc(d):
        import calendar
        return calendar.timegm(d.timetuple())
    self.response.out.write('%s\n%s\n%s' %(to_utc(project.start), to_utc(project.end), (project.end - project.start).days))
    

class FindMatches(webapp2.RequestHandler):
  def post(self):
    # send emails to erryone based on heuristic maximum funciton
    # if odd number, :(
    pass


class CreateProject(webapp2.RequestHandler):
  def post(self):
    def parse(time):
        return datetime.datetime.strptime(time, "%Y-%m-%d %H:%M")
    start = self.request.get('startdate')
    end = self.request.get('enddate')
    logging.info(start)
    start_time = parse(start)
    logging.info(start_time)
    end_time = parse(end)
    projects = Project.all_projects()
    response = projects.fetch(1)
    if response == []: 
        project = Project(parent=name_key('project'))
        project.start = start_time
        project.end = end_time
    else:
        project = response[0]
        project.start = start_time
        project.end = end_time
    project.put()
    
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'admin.html')
    template_values = {
    }
    self.response.out.write(template.render(path, template_values))


class Callback(webapp2.RequestHandler):
  def get(self):
    self.response.out.write(
    '''
    <script>
token = location.hash.split('token=')[1].split('&')[0];
window.location.href = 'http://group-40.appspot.com/getbusytimes?token='+token;
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

class GetBusyTimes(webapp2.RequestHandler):
  def get(self):
    token = self.request.get('token')
    timeMin = datetime.MINYEAR
    timeMax = datetime.MAXYEAR

    #data = dict([['access_token', token], ["timeMin", timeMin], ["timeMax",timeMax]])#, ["items", jsonTime(calendarIds)])
    response = urllib2.urlopen('https://www.googleapis.com/calendar/v3/users/me/calendarList?access_token='+token)
    response_text = response.read()
    cal_data = json.loads(response_text)
    calendarIds = []
    for calendar_list_entry in cal_data['items']:
        calendarIds.append({"id" : calendar_list_entry['id']})

    projects = Project.all_projects()
    response = projects.fetch(1)
    project = response[0]
    project.put()

    def jsonTime(time):
        return str(time).replace(" ", "T")+"Z"
    
    values = {
        'page_token' : token,
        'timeMin' : jsonTime(project.start),
        'timeMax' : jsonTime(project.end),
        'items' : calendarIds,
    }
    #logging.info(values)
    interval_list = [] # list of tuples - (start, end)
    def parse(time):
        time = time.rsplit('-', 1)[0]
        try:
            return datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            pass
    for cal_id in calendarIds:
        try:
            response = urllib2.urlopen('https://www.googleapis.com/calendar/v3/calendars/'+cal_id['id']+'/events?access_token='+token+'&timeMin='+values['timeMin']+'&timeMax='+values['timeMax'])
            response_text = response.read()
        except urllib2.HTTPError:
            continue
        event_data = json.loads(response_text)
        items = event_data['items']
        for item in items:
            try:
                (a, b) = (item['start']['dateTime'], item['end']['dateTime'])
                interval_list.append((parse(a), parse(b)))
            except KeyError:
                pass
    #data = urllib.urlencode(values)
    #data = str(values)
    #logging.info(data)
    #url = 'https://www.googleapis.com/calendar/v3/freeBusy'
    #req = urllib2.Request(url, data)
    #response = urllib2.urlopen(req)
    #response_text = response.read()
    #response = urllib2.urlopen('https://www.googleapis.com/calendar/v3/users/me/freeBusy?access_token='+token)

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
#if gmail then go to google cal selector else not
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
    ('/findmatches', FindMatches),
    ('/getbusytimes', GetBusyTimes),
    ('/oauth2callback', Callback),
    ('/getproject', GetProject),
    ('/createproject', CreateProject),
    ('/adduser', AddUser),
    ('/', MainHandler)
], debug=True)

