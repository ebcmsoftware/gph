$(document).ready(function() {

var CLIENT_ID = "887830103143-ptqtmjls6qvpgjdiv94h5g4oogd0230i.apps.googleusercontent.com"
/* CLIENT_ID = "887830103143-ptqtmjls6qvpgjdiv94h5g4oogd0230i.apps.googleusercontent.com"
    ClIENT_SECRET = "UQSES1KIMG_rmkPaqzpRUOcu"

    DEVELOPER_KEY = "AIzaSyBaZkVov0QHnKAmpjBV4Bl51FYtzDDFSJ4"
*/

$('#submitlogin').click(function() {
	post_params = {
        name: $('#studentname').val(),
        email: $('#studentemail').val(),
    }
    localStorage["email"] = post_params["email"];
    $.post('/adduser', post_params);
    window.location.href = "prefs.html";
});

$('#submit40').click(function() {
	post_params = {
        startdate: $('#sdate').val(),
        enddate: $('#edate').val(),
    }
	$.post('/createproject', post_params, function(){alert("yey");});
});

$('#submitprefs').click(function() {
    dayboxes = '';
    $('input').each(function(i, e) {
        if (e.type == 'checkbox') {
            dayboxes += e.checked ? ' 1' : ' 0';
        }
    });
    dayboxes = dayboxes.trim();
    post_params = {
    	email: localStorage["email"],
        free_days: dayboxes,
    };
    function success(data, textStatus, jqXHR) {
        console.log(data);
    }
    $.post('/addprefs', post_params, success);
});

//var OauthUrl = "https://accounts.google.com/o/oauth2/auth?scope=https://www.googleapis.com/auth/calendar.readonly&redirect_uri=http://group-40.appspot.com/oauth2callback&state=%2Fprofile&response_type=token&client_id=887830103143-ptqtmjls6qvpgjdiv94h5g4oogd0230i.apps.googleusercontent.com";
//https://accounts.google.com/o/oauth2/auth?scope=https://www.googleapis.com/auth/calendar.readonly&redirect_uri=http://group-40.appspot.com/oauth2callback&state=%2Fprofile&response_type=token&client_id=887830103143-ptqtmjls6qvpgjdiv94h5g4oogd0230i.apps.googleusercontent.com

$('#googbutton').click(function() {
	window.location.assign('https://accounts.google.com/o/oauth2/auth?scope=https://www.googleapis.com/auth/calendar.readonly&redirect_uri=http://group-40.appspot.com/oauth2callback&state=%2Fprofile&response_type=token&client_id=887830103143-ptqtmjls6qvpgjdiv94h5g4oogd0230i.apps.googleusercontent.com');
});
/*
console.log(google.gdata);
google.load("gdata", "2");
google.setOnLoadCallback(getMyFeed);
var feedUrl = "http://www.google.com/calendar/feeds/popcorncolonel@gmail.com/public/full";
*/
function setupMyService() {
  var myService = new google.gdata.calendar.CalendarService('exampleCo-exampleApp-1');
  return myService;
}

function getMyFeed() {
  myService = setupMyService();

  myService.getEventsFeed(feedUrl, handleMyFeed, handleError);
}

function logMeIn() {
  scope = "http://www.google.com/calendar/feeds/";
  var token = google.accounts.user.login(scope);
}

function setupMyService() {
  var myService = new google.gdata.calendar.CalendarService('exampleCo-exampleApp-1');
  logMeIn();
  return myService;
}
});
