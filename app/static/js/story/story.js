$(function() {
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
    if (this.location.pathname == '/story') {
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

    //Numbers only in year input
    $('#year-born-input').keypress(function (e) {
     if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
        return false;
     }
    });
    $('#year-death-input').keypress(function (e) {
     if (e.which == 116 || e.which == 84 || e.which == 116 || e.which == 111 || e.which == 79 || e.which == 100 || e.which == 68 || e.which == 116  || e.which == 97 || e.which == 65 || e.which == 121 || e.which == 89) {
         return true;
     } else if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
        return false;
     }
    });

    $("#first-name-field, #last-name-field, #user-first-name-field, #user-last-name-field").on('keyup', function() {
        capitalize(this.id, this.value)
    });

    // Media input type selection
    $('#image-upload-btn').click(function() {
        $('#story-video-input').hide();
        $('#story-image-input').show();
        $('#media-back-div').show();
        $('#image-upload-btn').hide();
        $('#video-upload-btn').hide();
    });
    $('#video-upload-btn').click(function() {
        $('#story-image-input').hide();
        $('#story-video-input').show();
        $('#media-back-div').show();
        $('#image-upload-btn').hide();
        $('#video-upload-btn').hide();
    });
    $('#media-back-div').click(function() {
        $('#media-back-div').hide();
        $('#story-image-input').hide();
        $('#story-video-input').hide();
        $('#image-upload-btn').show();
        $('#video-upload-btn').show();
        $('#story-image-input-box, #story-video-input-box').val("");
    });
});

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