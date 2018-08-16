$(function () {
    var tagRows = $('tr').toArray();
    var adding = false;

    $('#tag-add').parent().parent().hide();

    $.each(tagRows, function () {

        $(this).find('.tag-name').hide();
        $(this).find('#tag-update').hide();

        $(this).find('#tag-edit').click(function () {
            $(this).parent().parent().find('#tag-edit').toggle();
            $(this).parent().parent().find('#tag-remove').toggle();
            $(this).parent().parent().find('#tag-name').toggle();
            $(this).parent().parent().find('#tag-update').toggle();
            $(this).parent().parent().find('.tag-name').toggle();
        });

        $(this).find('#tag-update').click(function () {
            var id = $(this).attr("value");
            var name = $("#tag-name-" + id).val();

            getAjax(id, name, 'edit');

            $(this).parent().parent().find('#tag-name').text(name);
            $(this).parent().parent().find('#tag-edit').toggle();
            $(this).parent().parent().find('#tag-name').toggle();
            $(this).parent().parent().find('#tag-remove').toggle();
            $(this).parent().parent().find('.tag-name').toggle();
            $(this).toggle();
        });

        $(this).find('#tag-remove').click(function () {
            var id = $(this).attr("value");
            getAjax(id, null, 'remove');

            $(this).parent().parent().fadeOut(1000);
        });
    });
    
    $('.tag-add').click(function () {
        if(!adding){
            $('#tag-add').parent().parent().toggle();
            adding = true;
        }
    });

    $('#tag-add').click(function () {
        adding = false;
        var new_name = $('#tag-name-add').val();
        getAjax(null, new_name, 'add');
        $('#tag-name-add').val(' ');
        $('#tag-add').parent().parent().toggle();
    })

    $('#tag-cancel').click(function () {
        adding = false;
        $('#tag-name-add').val(' ');
        $('#tag-add').parent().parent().toggle();
    });
});

function getAjax(id, name, action){
    $.ajax({
        url: "/tag/update",
        type: "POST",
        data: {
            id: id,
            name: name,
            action: action
        },
        success: function() {
            window.location.reload();
            $(window).scrollTop(0);
        }
    });
}