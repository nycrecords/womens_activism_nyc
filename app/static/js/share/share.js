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
    var userPhone = $("#user-phone-field");
    var subscribe = $("#user-subscription-btn");

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

    // Prevents user from typing non numeric keys
    userPhone.keypress(function (key) {
        if (key.charCode !== 0) {
            if (key.charCode < 48 || key.charCode > 57) {
                key.preventDefault();
            }
        }
    });

    ///Format Field for Phone Number
    userPhone.mask("(999) 999-9999");

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
    userPhone.attr("data-parsley-maxlength", 25);

    userEmail.attr("data-parsley-type", "email");

    // Numbers only in year input or 'today' (case-insensitive)
    activistEnd.attr("data-parsley-error-message", "Please enter 'Today' or a numerical year.");
    activistEnd.attr("pattern", "\\b[Tt][Oo][Dd][Aa][Yy]\\b|^[0-9]{1,4}$");
    activistEnd.attr("data-parsley-pattern", "\\b[Tt][Oo][Dd][Aa][Yy]\\b|^[0-9]{1,4}$");

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

    $("#first-name-field, #last-name-field, #user-first-name-field, #user-last-name-field").on('keyup', function () {
        capitalize(this.id, this.value)
    });

    subscribe.attr('checked',function(){
        var requiredFields = [userEmail, userPhone];
        for (var i = 0; i < requiredFields.length; i++) {
            requiredFields[i].attr("data-parsley-required", "");
        }
        // Checks that at least one of the contact information fields is filled
        if (userEmail.parsley().isValid())
            // If at least one of the fields are validated then remove required from the rest of the contact fields that aren't being filled out
            userPhone.removeAttr("data-parsley-required");
        }
        else {
            // If none of the fields are valid then produce an error message and apply required fields.
            userEmail.attr("data-parsley-required", "");
            userPhone.attr("data-parsley-required", "");
        }
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
        $("#story-image-input-box, #story-video-input-box").val("");
    });

    $("#share-form").submit(function () {
        $("#share-story-btn").attr("disabled","disabled");
    })
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