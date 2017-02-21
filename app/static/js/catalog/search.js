$(function() {
    var start = 0,
        end = 0,
        total = 0,
        query = $("#query"),
        startInput = $("input[name='start']"),
        searchBtn = $("#search"),
        noResultsFound = true;

    function search() {
        // var results = $("#results");
        var results = $("#home-stories");

        $.ajax({
            url: "/search/stories",
            data: {
                query: query.val(),
                start: startInput.val()
            },
            success: function(data) {
                if (data.total !== 0) {
                    noResultsFound = false;
                    results.html(data.results)
                }
                else {
                    noResultsFound = true;

                }
            }
        });
    }

    search();

    function setStart(val) {
        start = val;
        $("input[name='start']").val(val);
    }

    $("#search-form").on("keyup, keypress", function(e){
        var keyCode = e.keyCode || e.which;
        if (keyCode === 13) {
            e.preventDefault();
            return false;
        }
    });

    searchBtn.click(function() {
        search();
    })
});