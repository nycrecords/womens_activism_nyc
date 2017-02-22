$(function () {
    // Initialize global variables
    var start = 0,
        total = 0,
        size = null,
        append = false,
        query = $("#catalog-search"),
        startInput = $("input[name='start']"),
        searchBtn = $("#catalog-search-btn"),
        noResultsFound = true;

    // Search function
    function search() {
        var results = $("#home-stories");

        $.ajax({
            url: "/search/stories",
            type: "GET",
            data: {
                query: query.val(),
                size: size,
                start: startInput.val()
            },
            success: function (data) {
                if (data.total !== 0 && !append) {
                    noResultsFound = false;
                    results.html(data.results);
                    start = start + data.count;
                    total = data.total;
                }
                else if (data.total !== 0 && append ) {
                    noResultsFound = false;
                    results.append(data.results);
                    start = start + data.count;
                }
                else {
                    noResultsFound = true;
                    results.html("<div>No results found.</div>")
                }
            }
        });
    }

    // Search on page load
    search();

    // Set value of hidden start input
    function setStart(val) {
        start = val;
        startInput.val(val);
    }

    // Resets all previous search results and call search method
    function resetAndSearch() {
        setStart(0);
        size = null;
        append = false;
        search()
    }

    // Upon hitting enter on search input, click search button
    query.keyup(function(e){
        if (e.keyCode === 13) {
            searchBtn.click();
        }
    });

    // Validate search input field and if valid, call resetAndSearch method
    searchBtn.click(function () {
        query.parsley().validate();
        if (query.parsley().isValid()) {
            resetAndSearch();
        }
    });

    // Call search method upon scrolling to bottom of page
    $(window).scroll(function () {
        if ($(window).scrollTop() == $(document).height() - $(window).height() && (start < total)) {
            setStart(start);
            size = 20;
            append = true;
            search();
        }
    });
});