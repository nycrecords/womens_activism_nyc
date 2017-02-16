window.onload = function() {
    var hiddenTagInput = $('#hidden-tag-input');

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
        hiddenTagInput.val(selectedTags);

        hiddenTagInput.parsley().validate();
    });

    // Share a story - text counter
    $('#her-story-text').keyup(function () {
        $('#story-text-count').text($(this).val().length);
    });

    //Nav active state change
    $(".nav li").removeClass("active");
    $('a[href=".' + this.location.pathname + '"]').parents('li,ul').addClass('active');

    // Scroll fix for Parsley.js
    if (this.location.pathname == '/share') {
      var errorList = [];
      window.Parsley.on('field:error', function() {
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
};

// Share a story - capitalize first letter of name inputs
function capitalize(textboxid, str) {
  // string with alteast one character
  if (str && str.length >= 1)
  {
      var firstChar = str.charAt(0);
      var remainingStr = str.slice(1);
      str = firstChar.toUpperCase() + remainingStr;
  }
  document.getElementById(textboxid).value = str;
}