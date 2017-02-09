window.onload = function() {
  // Functionality for tags
  var selectedTags = [];

  $('.share-tag').click(function() {
    $(this).toggleClass('share-inactive');
    $(this).toggleClass('share-active');
    if ($.inArray(this.childNodes[0].data, selectedTags) > -1) {
      selectedTags.splice($.inArray(this.childNodes[0].data, selectedTags), 1);
    } else {
      selectedTags.push(this.childNodes[0].data);
    }
    console.log(selectedTags);
  });

  // Share a story - text counter

  $('#her-story-text').keyup(function() {
    $('#story-text-count').text($(this).val().length);
  });
}
