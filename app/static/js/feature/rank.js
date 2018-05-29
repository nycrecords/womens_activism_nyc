$(function() {
    $('#rankTable input.move').click(function() {
    var row = $(this).closest('tr');
    if ($(this).hasClass('up'))
        row.prev().before(row);
    else
        row.next().after(row);
    });
});

function rowName(x) {
    console.log("Row index is: " + x.rowIndex);
}



