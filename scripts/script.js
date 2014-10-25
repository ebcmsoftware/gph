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
    localStorage.setItem("gphemail", $('#studentemail').val());
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
	console.log("YO");
	alert($("#freeTimes").html());
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
    //window.location.assign('success.html');
    $.post('/addprefs', post_params, success);
});

$('#sendmatches').click(function() {
	$.post('/dothematches', "yo just give me a fucking cron job ;)");
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
