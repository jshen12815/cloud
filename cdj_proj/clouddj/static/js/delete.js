$(document).ready(function() {
$("#del-btn").click(function( event ) {

    var link = $(this).parent();
    var url = link.attr("href");

    $.ajax({
        url: url,

        success: function( data ) {

            var post_id = data['post_id'];
            link.parent().parent().parent().hide();
        }
    });

    return false;
});
});