window.onload = function() {
  $(".share-tag" ).click(function() {
    $(this).toggleClass('share-inactive');
    $(this).toggleClass('share-active');
  });
}
