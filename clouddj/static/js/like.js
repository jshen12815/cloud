$(document).ready(function() {
$(".like-btn").click(function( event ) {

    var form = $(".comm-form");
    var url = $(this).parent().attr("href");
    var csrf_name = form.find("[type=hidden]").attr("name");
    var like_button = $(this);

    $.ajax({
        url: url,

        data: {
            "csrfmiddlewaretoken": $("#csrf").val()
        },

        type: "POST",

        success: function( data ) {
            var post_id = data['post_id'];
            var count = parseInt($("#"+post_id).parent().parent().prev().find(".like-count").html());
            if (data['liked'] == "True") {
                like_button.addClass("lit-like");
                like_button.html("&#10084 Unlike");
                $("#"+post_id).parent().parent().prev().find(".like-count").html((count + 1).toString());
            }
            if (data['unliked'] == "True") {
                like_button.removeClass("lit-like");
                like_button.html("&#10084 Like");
                $("#"+post_id).parent().parent().prev().find(".like-count").html((count - 1).toString());
            }
        }
    });

    return false;
});
});