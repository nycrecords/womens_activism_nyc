$(function() {
    var titleInput = $("#title");
    var descriptionInput = $("#description");

    var requiredFields = ["title", "description"];
    for (var i = 0; i < requiredFields.length; i++) {
        $("#" + requiredFields[i]).attr("data-parsley-required","");
    }

    // Specify length requirement of certain fields
    titleInput.attr("data-parsley-maxlength", 90);
    descriptionInput.attr("data-parsley-maxlength", 365);
});
