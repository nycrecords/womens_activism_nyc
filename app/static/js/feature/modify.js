$(function() {
    var titleInput = $("#title");
    var descriptionInput = $("#description");

    var requiredFields = ["title", "description"];
    for (var i = 0; i < requiredFields.length; i++) {
        $("#" + requiredFields[i]).attr("data-parsley-required","");
    }

    // Specify length requirement of certain fields
    titleInput.attr("data-parsley-maxlength", 90);
    descriptionInput.attr("data-parsley-maxlength", 395);

    // var errorList = [];
    // window.Parsley.on('field:error', function () {
    //     if (!errorList[0]) {
    //         errorList.push(this.$element);
    //         $("html, body").animate({
    //             scrollTop: errorList[0].parent().parent().parent().find('h1').offset().top
    //         }, 1000, function () {
    //             errorList = [];
    //         });
    //     }
    // });
})