$(document).ready(function() {
$(".del-btn").click(function( event ) {

    var url = $(this).parent().attr("href");

    $.ajax({
        url: url,

        success: function( data ) {

            var post_id = data['post_id'];
            $("#"+post_id).parent().parent().next().remove();
            $("#"+post_id).parent().parent().remove();
        }
    });

    return false;
});
});