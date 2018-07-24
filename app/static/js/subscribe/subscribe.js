$(function () {
    var userFirst = $("#user-first-name-field");
    var userLast = $("#user-last-name-field");
    var userEmail = $("#user-email-field");
    var userPhone = $("#user-phone-field");

    // Nav active state change
    $(".nav li").removeClass("active");
    $('a[href=".' + this.location.pathname + '"]').parents('li,ul').addClass('active');

    // Prevents user from typing non numeric keys
    $("#user-phone-field").keypress(function (key) {
        if (key.charCode !== 0) {
            if (key.charCode < 48 || key.charCode > 57) {
                key.preventDefault();
            }
        }
    });

    ///Format Field for Phone Number
    $("#user-phone-field").mask("(999) 999-9999");

    // Loop through required fields and apply a data-parsley-required attribute to them
    var requiredFields = ["user-email-field", "user-phone-field"];
    for (var i = 0; i < requiredFields.length; i++) {
        $("#" + requiredFields[i]).attr("data-parsley-required", "");
    }

    // Specify length requirement of certain fields
    userFirst.attr("data-parsley-maxlength", 128);
    userLast.attr("data-parsley-maxlength", 128);
    userEmail.attr("data-parsley-maxlength", 254);
    userPhone.attr("data-parsley-maxlength", 25);

    userEmail.attr("data-parsley-type", "email");

    $("#user-first-name-field, #user-last-name-field").on('keyup', function () {
        capitalize(this.id, this.value)
    });


    $("#subscribe-form").submit(function () {
        $("#subscribe-btn").attr("disabled", "disabled");
    });

    $("#subscribe-form").parsley().on("form:validate", function () {

        if ($("#userPhone").parsley().isValid() ||
        $("#userEmail").parsley().isValid()
    ) {
        // If at least one of the fields are validated then remove required from the rest of the contact fields that aren't being filled out
        $("#userEmail").removeAttr("data-parsley-required");
        $("#userPhone").removeAttr("data-parsley-required")
    }
    else {
        // If none of the fields are valid then apply required fields.
        $("#userPhone").attr("data-parsley-required", "");
        $("#userEmail").attr("data-parsley-required", "")
    }

    });


});
