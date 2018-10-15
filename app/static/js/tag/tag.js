$(function () {
    var tagRows = $('tr').toArray();

    //Hides the new tag input
    $('#tag-add').parent().parent().hide();

    $.each(tagRows, function () {

        //Hides the editing input
        $(this).find('.tag-name').hide();
        $(this).find('.tag-update').hide();

        //Switches to the editing input when the edit button is clicked
        $(this).find('#tag-edit').click(function () {
            $(this).parent().parent().find('#tag-edit').toggle();
            // $(this).parent().parent().find('.tag-remove').toggle();
            $(this).parent().parent().find('#tag-name').toggle();
            $(this).parent().parent().find('.tag-update').toggle();
            $(this).parent().parent().find('.tag-name').toggle();
        });

        //Updates tag
        $(this).find('.tag-update').click(function () {
            var id = $(this).attr("id");
            var name = $("#tag-name-" + id).val();

            getAjax(id, name, 'edit');
        });

        //Removes tag
        // $(this).find('.tag-remove').click(function () {
        //     var id = $(this).attr("id");
        //     getAjax(id, null, 'remove');
        // });
    });

    //Shows the new tag input
    $('.tag-add').click(function () {
        $('#tag-add').parent().parent().show();
    });

    //Adds new tag
    $('#tag-add').click(function () {
        var new_name = $('#tag-name-add').val();
        $('#tag-name-add').val(' ');
        getAjax(null, new_name, 'add');
    });

    //Hides new tag input
    $('#tag-cancel').click(function () {
        $('#tag-name-add').val(' ');
        $('#tag-add').parent().parent().hide();
    });
});

//Sends data to backend
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
