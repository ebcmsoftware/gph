$(document).ready(function() {

$('#submitbtn').click(function() {
    dayboxes = '';
    $('input').each(function(i, e) {
        if (e.type == 'checkbox') {
            dayboxes += e.checked ? ' 1' : ' 0';
        }
    });
    dayboxes = dayboxes.trim();
    $.post('/adduser', dayboxes);
});

});
