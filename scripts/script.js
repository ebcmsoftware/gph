$(document).ready(function() {

dayboxes = '';
$('input').each(function(i, e) {
    if (e.type == 'checkbox') {
        dayboxes += ' ' + e.value;
    }
});
dayboxes = dayboxes.strip();
console.log(dayboxes);
$.post('/adduser', dayboxes);

});
