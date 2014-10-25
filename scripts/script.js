$(document).ready(function() {

$('#submitlogin').click(function() {
	post_params = {
        name: $('#studentname').val(),
        email: $('#studentemail').val(),
    }
    localStorage["email"] = post_params["email"];
    $.post('/adduser', post_params);
    window.location.href = "prefs.html";
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


});
