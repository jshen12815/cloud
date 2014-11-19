$(document).ready(function() {
$("#del-btn").click(function( event ) {

    var link = $(this).parent();
    var url = link.attr("href");
    var element = $(this);

    $.ajax({
        url: url,

        success: function( data ) {

            var post_id = data['post_id'];
            element.parent().parent().parent().parent().remove();
        }
    });

    return false;
});
});