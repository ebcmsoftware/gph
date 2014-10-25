$(document).ready(function() {

$('#submitbtn').click(function() {
    dayboxes = '';
    $('input').each(function(i, e) {
        if (e.type == 'checkbox') {
            dayboxes += e.checked ? ' 1' : ' 0';
        }
    });
    dayboxes = dayboxes.trim();
    post_params = {
        name: $('#studentname').val(),
        email: $('#studentemail').val(),
        free_days: dayboxes,
    };
    function success(data, textStatus, jqXHR) {
        console.log(data);
    }
    $.post('/adduser', post_params, success);
});

});
