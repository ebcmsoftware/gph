$(document).ready(function() {

var CLIENT_ID = "887830103143-ptqtmjls6qvpgjdiv94h5g4oogd0230i.apps.googleusercontent.com"

$('#submitlogin').click(function() {
    var email = $('#studentemail').val() 
    var name = $('#studentname').val(),
	post_params = {
        name: name,
        email: email,
    }
    localStorage.setItem("gphemail", email);
    if (name == '') {
        alert("Please enter your name.");
        return;
    }
    if (email.match(/\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b/gi) != null) {
        $.post('/adduser', post_params);
        window.location.href = "/prefs";
    } else {
        alert("That's not an email address.");
    }
});

$('#submit40').click(function() {
	post_params = {
        startdate: $('#sdate').val(),
        enddate: $('#edate').val(),
    }
	$.post('/createproject', post_params);
});

$('#submitprefs').click(function() {
    post_params = {
    	email: localStorage.getItem("gphemail"),
        free_times: $("#freeTimes").val(),
    	timeofday: $("input[name=timeofday]:checked").val(),
    	whotypes: $("input[name=whotypes]:checked").val(),
    	texteditor: $("input[name=texteditor]:checked").val(),
    	classyear: $("input[name=classyear]:checked").val(),
    };
    console.log(post_params);
    function success(data, textStatus, jqXHR) {
        console.log(data);
    }
    window.location.assign('/success');
    $.post('/addprefs', post_params, success);
});

$('#sendmatches').click(function() {
	$.post('/matchmake', "hey lets send out some emails;)");
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
