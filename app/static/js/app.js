window.onload = function() {
    console.log('app.js');
    // Functionality for tags
    var selectedTags = [];

    $('.share-tag').click(function () {
        $(this).toggleClass('share-inactive');
        $(this).toggleClass('share-active');
        if ($.inArray(this.childNodes[0].data, selectedTags) > -1) {
            selectedTags.splice($.inArray(this.childNodes[0].data, selectedTags), 1);
        } else {
            selectedTags.push(this.childNodes[0].data);
        }
        console.log(selectedTags);
        $('#hidden-tag-input').val(selectedTags);
    });

    // Share a story - text counter

    $('#her-story-text').keyup(function () {
        $('#story-text-count').text($(this).val().length);
    });

    //Nav active state change
    $(".nav li").removeClass("active");
    $('a[href=".' + this.location.pathname + '"]').parents('li,ul').addClass('active');


    if (this.location.pathname == '/share') {
      console.log('share');
      // $(document).ready(function() {
      //   $.listen('parsley:field:error', function(parsleyField) {
      //     console.log('test');
      //     return $("html, body").animate({
      //       scrollTop: parsleyField.$element.offset().top
      //     }, 1000);
      //   });
      // });
      var errorList = [];
      window.Parsley.on('field:error', function() {
        // This global callback will be called for any field that fails validation.
        if (!errorList[0]) {
            errorList.push(this.$element);
            $("html, body").animate({
                scrollTop: errorList[0].parent().parent().parent().find('h1').offset().top
            }, 1000, function () {
                errorList = [];
            });
        }
      });
    }
}