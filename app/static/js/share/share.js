$(function () {
    var hiddenTagInput = $("#hidden-tag-input");
    var shareTag = $(".share-tag");
    var imageButton = $("#image-upload-btn");
    var videoInput = $("#story-video-input");
    var imageInput = $("#story-image-input");
    var videoButton = $("#video-upload-btn");
    var mediaButton = $("#media-back-div");
    var activistFirst = $("#first-name-field");
    var activistLast = $("#last-name-field");
    var activistStart = $("#activist-start");
    var activistEnd = $("#activist-end");
    var userFirst = $("#user-first-name-field");
    var userLast = $("#user-last-name-field");
    var userEmail = $("#user-email-field");

    // Functionality for tags
    var selectedTags = [];

    shareTag.click(function () {
        $(this).toggleClass("share-inactive");
        $(this).toggleClass("share-active");
        var index = selectedTags.indexOf(this.value);
        // Append value of active buttons to array, remove if inactive
        if(index > -1) {
            selectedTags.splice(index, 1);
        }
        else {
            selectedTags.push(this.value);
        }
        // Append array to hidden share tag input
        hiddenTagInput.val(selectedTags);
    });

    // Nav active state change
    $(".nav li").removeClass("active");
    $('a[href=".' + this.location.pathname + '"]').parents('li,ul').addClass('active');

    // Loop through required fields and apply a data-parsley-required attribute to them
    var requiredFields = ["first-name-field", "last-name-field", "hidden-tag-input", "story-content"];
    for (var i = 0; i < requiredFields.length; i++) {
        $("#" + requiredFields[i]).attr("data-parsley-required", "");
    }

    // Set buttons to active if hiddenTagInput has value (backend validation for form fails)
    if (hiddenTagInput.val()) {
        selectedTags = hiddenTagInput.val().split(',');
        for (i = 0; i < selectedTags.length; i++) {
            var activeButton = $("button[value=" + selectedTags[i] + "]");
            activeButton.toggleClass("share-inactive");
            activeButton.toggleClass("share-active");
        }
    }

    // Specify length requirement of certain fields
    activistFirst.attr("data-parsley-maxlength", 64);
    activistLast.attr("data-parsley-maxlength", 64);
    hiddenTagInput.attr("data-parsley-maxlength", 500);
    userFirst.attr("data-parsley-maxlength", 128);
    userLast.attr("data-parsley-maxlength", 128);
    userEmail.attr("data-parsley-maxlength", 254);

    userEmail.attr("data-parsley-type", "email");

    // Scroll fix for Parsley.js
    var errorList = [];
    window.Parsley.on('field:error', function () {
        shareTag.click(function(){
            hiddenTagInput.parsley().validate()
        });
        if (!errorList[0]) {
            errorList.push(this.$element);
            $("html, body").animate({
                scrollTop: errorList[0].parent().parent().parent().find('h1').offset().top
            }, 1000, function () {
                errorList = [];
            });
        }
    });

    // Numbers only in year input
    activistStart.keypress(function (e) {
        if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
            return false;
        }
    });
    activistEnd.keypress(function (e) {
        if (e.which == 116 || e.which == 84 || e.which == 116 || e.which == 111 || e.which == 79 || e.which == 100 || e.which == 68 || e.which == 116 || e.which == 97 || e.which == 65 || e.which == 121 || e.which == 89) {
            return true;
        } else if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
            return false;
        }
    });

    $("#first-name-field, #last-name-field, #user-first-name-field, #user-last-name-field").on('keyup', function () {
        capitalize(this.id, this.value)
    });

    // Media input type selection
    imageButton.click(function () {
        videoInput.hide();
        imageInput.show();
        mediaButton.show();
        imageButton.hide();
        videoButton.hide();
    });
    videoButton.click(function () {
        imageInput.hide();
        videoInput.show();
        mediaButton.show();
        imageButton.hide();
        videoButton.hide();
    });
    mediaButton.click(function () {
        mediaButton.hide();
        imageInput.hide();
        videoInput.hide();
        imageButton.show();
        videoButton.show();
        // $("#story-image-input-box, #story-video-input-box").val("");
    });
});

// Share a story - capitalize first letter of name inputs
function capitalize(textboxid, str) {
    // string with alteast one character
    if (str && str.length >= 1) {
        var firstChar = str.charAt(0);
        var remainingStr = str.slice(1);
        str = firstChar.toUpperCase() + remainingStr;
    }
    document.getElementById(textboxid).value = str;
}