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
import schedule

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
  email = ndb.StringProperty()
  #free_days = ndb.StringProperty(default='0 0 0 0 0 0 0')
  text_editor = ndb.StringProperty(default='')
  year = ndb.IntegerProperty(default=0) # 0 = freshman, ..., 4 = grad student
  sleep_hours = ndb.StringProperty(default='')
  busy_times = ndb.StringProperty(repeated=True)

  @classmethod
  def query_users(self, email):
    return self.query(ancestor=email)

  @classmethod
  def all_users(self):
    return self.query()

def send_email(email=None, match_name=None, match_email=None, reasons=None):
    if email not in ("", None) and match_name not in ("", None) and match_email not in ('', None):
        bod = """We've matched you with %s for the following reasons:
              """ % (match_name)
        for r in reasons:
            bod += r + """ {0}
                        """.format(reasons[r])
            bod += """
            this is their email address: %s
            """ % match_email
        mail.send_mail(sender="the <x> team (change this) <popcorncolonel@gmail.com>",
                       to=email,
                       subject="We've found you a project partner!",
                       body= bod)
    

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
    

class Matchmake(webapp2.RequestHandler):
  def get(self):
    # send emails to erryone based on heuristic maximum funciton
    # if odd number, :(
    users = User.all_users()
    s = schedule.Schedule()
    for user in users:
        for interval in user.busy_times:
            try:
                [a, b] = json.loads(interval)
                self.response.out.write([a, b])
            except:
                logging.debug('no')
            #[start, end] = json.loads(interval)
        #l = json.loads(busy_list)
        #self.response.out.write(l)
        continue


    def findFreeTimesAmongstBusy(self, timePeriods, startTime, endTime):
        startTimes=[startTime]
        endTimes=[]
        for time in timePeriods:
            freeUntil=True
            freeAfter=True
            for time2 in timePeriods:
                if(time[0] > time2[0] and time[0] < time2[1]):
                    freeUntil=False
                if(time[1] > time2[0] and time[1] < time2[1]):
                    freeAfter=False
            if(freeUntil):
                endTimes.append(time[0])
            if(freeAfter):
                startTimes.append(time[1])
        startTimes.sort()
        endTimes.sort()
        endTimes.append(endTime)
        freeTimes=[]
        for i in range(len(startTimes)):
            freeTimes.append((startTimes[i],endTimes[i]))
        return freeTimes

  def post(self):
    def to_utc(d):
        import calendar
        return calendar.timegm(d.timetuple())
    # send emails to erryone based on heuristic maximum funciton
    # if odd number, :(
    users = User.all_users()
    s = schedule.Schedule({'editor':0.5, 'year':0.5})
    for user in users:
        busy_list = user.busy_times
        interval_list = []
        for interval in busy_list:
            fmt_str = "%Y-%m-%dT%H:%M:%S"; 
            try:
                i = json.loads(interval)
                (a, b) = (datetime.datetime.strptime(i[0], fmt_str), 
                          datetime.datetime.strptime(i[1], fmt_str))
            except (IndexError, ValueError):
                continue
            interval_list.append([to_utc(a),to_utc(b)])
        if interval_list != []:
            s.add_student(user.email, interval_list, preferences={'editor':user.texteditor, 'year':user.year}, time_weights=[])
            logging.info(interval_list)
    pairs = schedule.pair_students(s)
    for (email1, email2, reasons) in pairs:
        user_query = User.query_users(email=email_key(email2))
        response = user_query.fetch(1)
        user2 = response[0]
        send_email(email1, user2.name, email2, reasons)

        user_query = User.query_users(email=email_key(email1))
        response = user_query.fetch(1)
        user1 = response[0]
        send_email(email2, user1.name, email1, reasons)
    #we have a done schedj yeeeeeeeeeeeeee


class CreateProject(webapp2.RequestHandler):
  def post(self):
    def parse(time):
        return datetime.datetime.strptime(time, "%Y-%m-%d %H:%M")
    start = self.request.get('startdate')
    end = self.request.get('enddate')
    start_time = parse(start)
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

    
class Success(webapp2.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'success.html')
    template_values = {
    }
    self.response.out.write(template.render(path, template_values))


class Callback(webapp2.RequestHandler):
  def get(self):
    self.response.out.write(
    '''
    <script>
token = location.hash.split('token=')[1].split('&')[0];
window.location.href = 'http://group-40.appspot.com/getbusytimes?token='+token+'&email='+localStorage['gphemail'];
</script>
    ''')

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
    email = self.request.get('email')
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
    interval_list = [] # list of tuples - (start, end)
    def parse(time):
        time = time.rsplit('-', 1)[0]
        try:
            return time 
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
                a = parse(a)
                b = parse(b)
                if a and b and a != '' and b != '':
                    interval = json.dumps([a, b]) 
                    interval_list.append(interval)
            except KeyError:
                pass
    user_query = User.query_users(email=email_key(email))
    response = user_query.fetch(1)
    user = response[0]
    user.busy_times = interval_list
    user.put()
    self.redirect('/prefs')


class Prefs(webapp2.RequestHandler):
  def get(self):
    # pair people with other people
    path = os.path.join(os.path.dirname(__file__), 'prefs.html')
    template_values = {
    }
    self.response.out.write(template.render(path, template_values))
    return


class MainHandler(webapp2.RequestHandler):
  def get(self):
    # pair people with other people
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    template_values = {
    }
    self.response.out.write(template.render(path, template_values))
    return


class AddPrefs(webapp2.RequestHandler):
  def post(self):
    texteditor = self.request.get('texteditor')
    classyear = self.request.get('classyear')
    email = self.request.get('email')
    user_query = User.query_users(email=email_key(email))
    response = user_query.fetch(1)

    years = {
        'freshman':0,
        'sophomore':1,
        'junior':2,
        'senior':3,
        'oldguys':4,
    }
    try:
        user = response[0]
        user.texteditor = texteditor
        user.year = years[classyear]
    except IndexError:
        return
    user.put()


class AddUser(webapp2.RequestHandler):
  def post(self):
    name = self.request.get('name')
    email = self.request.get('email')
    try:
        (x, site) = email.split('@')
        machine = site.split('.')[1]
    except IndexError:
        self.redirect('/')
        return
    user_query = User.query_users(email=email_key(email))
    response = user_query.fetch(1)
    if response == []: #create a new user
        user = User(parent=email_key(email))
        user.name = name
        user.email = email
    else:
        user = response[0]
    user.put()

app = webapp2.WSGIApplication([
    ('/matchmake', Matchmake),
    ('/getbusytimes', GetBusyTimes),
    ('/oauth2callback', Callback),
    ('/getproject', GetProject),
    ('/createproject', CreateProject),
    ('/success', Success),
    ('/adduser', AddUser),
    ('/addprefs', AddPrefs),
    ('/prefs', Prefs),
    ('/', MainHandler)
], debug=True)

