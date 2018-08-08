$('#rightArrow').click(function() {
    $('#tweetsRow').animate({
        scrollLeft:"+="+380+"px"
    }, 'slow', function() {

        $('html, body').animate({
            scrollLeft: 0
        }, 800);

    });
});

$('#leftArrow').click(function() {
    $('#tweetsRow').animate({
        scrollLeft:"-="+380+"px"
    }, 800, function() {

        $('html, body').animate({
            scrollLeft: 0
        }, 800);

    });
});
