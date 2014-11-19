$(document).ready(function() {
$(".like-btn").click(function( event ) {

    var form = $(".comm-form");
    var url = $(this).parent().attr("href");
    var csrf_name = form.find("[type=hidden]").attr("name");

    $.ajax({
        url: url,

        data: {
            "csrfmiddlewaretoken": $("#csrf").val()
        },

        type: "POST",

        success: function( data ) {
            var post_id = data['post_id'];
            var like_button = $("#"+post_id).prev().find(".like-btn");
            var count = parseInt($("#"+post_id).prev().find(".like-count").html());
            if (data['liked'] == "True") {
                like_button.addClass("lit-like");
                $("#"+post_id).prev().find(".like-count").html((count + 1).toString());
            }
            if (data['unliked'] == "True") {
                like_button.removeClass("lit-like");
                $("#"+post_id).prev().find(".like-count").html((count - 1).toString());
            }
        }
    });

    return false;
});
});