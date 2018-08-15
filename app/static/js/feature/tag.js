$(function () {
    var tagRows = $('tr').toArray();
    var updateButtons = $('.tag-update').toArray();

    $.each(tagRows, function () {

        $(this).find('.tag-name').hide();
        $(this).find('.tag-update').hide();

        $(this).find('#edit').click(function () {
            $(this).parent().parent().find('#edit').toggle();
            $(this).parent().parent().find('#name').toggle();
            $(this).parent().parent().find('.tag-name').toggle();
            $(this).parent().parent().find('.tag-update').toggle();
        });
    });

    var successmessage;

    $.each(updateButtons, function () {
        $(this).click(function () {
            var id = $(this).attr('id');
            var name = $('tag-name-'+id).val();

            $.ajax({
                url : "/tag/update",
                type: "POST",
                data: {
                    id: id,
                    name: name
                },
                success: function (data) {
                    debugger;
                    successmessage = 'success';
                    alert(successmessage);
                }
            });

            $(this).parent().parent().find('#name').text(name);
            $(this).parent().parent().find('#edit').toggle();
            $(this).parent().parent().find('#name').toggle();
            $(this).parent().parent().find('.tag-name').toggle();
            $(this).toggle();
        });
    });
});