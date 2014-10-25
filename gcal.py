import gflags
import httplib2
import json

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
from dateutil.parser import parse

def jsonTime(time):
    return str(time).replace(" ", "T")+"Z"

def findFreeTimesAmongstBusy(timePeriods, startTime, endTime):
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
           
def getGoogleFreeTime(timeMin, timeMax):
    
    FLAGS = gflags.FLAGS


    CLIENT_ID = "887830103143-ptqtmjls6qvpgjdiv94h5g4oogd0230i.apps.googleusercontent.com"
    ClIENT_SECRET = "UQSES1KIMG_rmkPaqzpRUOcu"

    DEVELOPER_KEY = "AIzaSyBaZkVov0QHnKAmpjBV4Bl51FYtzDDFSJ4"

    # Set up a Flow object to be used if we need to authenticate. This
    # sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
    # the information it needs to authenticate. Note that it is called
    # the Web Server Flow, but it can also handle the flow for native
    # applications
    # The client_id and client_secret can be found in Google Developers Console
    FLOW = OAuth2WebServerFlow(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scope='https://www.googleapis.com/auth/calendar.readonly',
        user_agent='Group40/1.0')

    # To disable the local server feature, uncomment the following line:
    FLAGS.auth_local_webserver = False

    # If the Credentials don't exist or are invalid, run through the native client
    # flow. The Storage object will ensure that if successful the good
    # Credentials will get written back to a file.
    storage = Storage('calendar.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid == True:
    credentials = run(FLOW, storage)

    # Create an httplib2.Http object to handle our HTTP requests and authorize it
    # with our good Credentials.
    http = httplib2.Http()
    http = credentials.authorize(http)

    # Build a service object for interacting with the API. Visit
    # the Google Developers Console
    # to get a developerKey for your own application.
    service = build(serviceName='calendar', version='v3', http=http,
        developerKey=DEVELOPER_KEY)
    
    calendarIds=[]
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            calendarIds.append({"id",calendar_list_entry['id']})
        page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break
    
    data = dict(["timeMin", timeMin], ["timeMax",jsonTime(timeMax)], ["items", jsonTime(calendarIds)])
    (resp, content) = http.request("https://www.googleapis.com/calendar/v3/freeBusy", "POST", urlencode(json.dumps(data)))
    
    
    content=json.loads(content)
    
    timePeriods=[]
    
    for cal in content["calendars"]:
        begining=true
        calendar=[]
        for time in content["calendars"][cal]["busy"]:
            timePeriods.append([parse(time["start"]),parse(time["end"])])
         
    return findFreeTimesAmongstBusy(timePeriods, timeMin, timeMax)
     
    
         
    
    
    
    
    
    
