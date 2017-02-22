$(function () {
    var catalogTag = $('.catalog-tag');
    var hiddenCatTagInput = $('#hidden-catalog-tag-input');

    // Functionality for tags
    var selectedCatTags = [];

    catalogTag.click(function () {
        $(this).toggleClass('catalog-tag-inactive');
        $(this).toggleClass('catalog-tag-active');
        if ($.inArray(this.childNodes[0].data, selectedCatTags) > -1) {
            selectedCatTags.splice($.inArray(this.childNodes[0].data, selectedCatTags), 1);
        } else {
            selectedCatTags.push(this.childNodes[0].data);
        }
        hiddenCatTagInput.val(selectedCatTags.join(';'));
    });

});