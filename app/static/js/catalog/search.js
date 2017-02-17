$(function() {
    var start = 0,
        end = 0,
        total = 0,
        searchBtn = $("#search"),
        noResultsFound = true;

    function search() {
        var results = $("#results");

        $.ajax({
            url: "/search/stories",
            data: $("#search-form").serializeArray()
        });
    }

    search();
});