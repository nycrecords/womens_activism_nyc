$(function () {
    var userEmail = $("#user-email-field");
    var userPhone = $("#user-phone-field");

    // Prevents user from typing non numeric keys
    userPhone.keypress(function (key) {
        if (key.charCode !== 0) {
            if (key.charCode < 48 || key.charCode > 57) {
                key.preventDefault();
            }
        }
    });

    // Format Field for Phone Number
    userPhone.mask("(999) 999-9999");

    // Loop through required fields and apply a data-parsley-required attribute to them
    var requiredFields = [userEmail, userPhone];

    for (var i = 0; i < requiredFields.length; i++) {
        requiredFields[i].attr("data-parsley-required", "");
    }

    // Specify length requirement of certain fields
    userEmail.attr("data-parsley-maxlength", 254);
    userPhone.attr("data-parsley-maxlength", 25);

    userEmail.attr("data-parsley-type", "email");

    // Enter an email or phone number error
     userPhone.attr("data-parsley-error-message", "Email and/or phone number is required.");
     userEmail.attr("data-parsley-error-message", "Email and/or phone number is required.");

    $("#unsubscribe-form").parsley().on("form:validate", function () {
        // Re-apply validators to fields in the event that they were removed from previous validation requests.
        for (i = 0; i < requiredFields.length; i++) {
            requiredFields[i].attr("data-parsley-required", "");
        }
        // Checks that at least one of the contact information fields is filled
        if (userEmail.parsley().isValid() || userPhone.parsley().isValid()) {
            // If at least one of the fields are validated then remove required from the rest of the contact fields that aren't being filled out
            userEmail.removeAttr("data-parsley-required");
            userPhone.removeAttr("data-parsley-required");
        }
        else {
            // If none of the fields are valid then produce an error message and apply required fields.
            userEmail.attr("data-parsley-required", "");
            userPhone.attr("data-parsley-required", "");
        }
    });

});
