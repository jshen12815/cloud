$(document).ready(function() {
    $(".starrate").click(function( event ) {

        var form = $(".rateform");
        var url = $(this).parent().attr("href");
        //var csrf_name = form.find("[type=hidden]").attr("name");
        console.log(url);
        
        $.ajax({
            url: url,

            data: {
                "csrfmiddlewaretoken": $("#csrf").val()
            },

            type: "POST",

            success: function( data ) {
                console.log("ok, thing successful?");
                var post_id = data['post_id'];
                var like_button = $("#"+post_id).prev().find(".like-btn");
                var count = parseInt($("#"+post_id).prev().find(".like-count").html());
                if (data['liked'] == "True") {
                    like_button.addClass("lit-like");
                    like_button.html("&#10084 Unlike");
                    $("#"+post_id).prev().find(".like-count").html((count + 1).toString());
                }
                if (data['unliked'] == "True") {
                    like_button.removeClass("lit-like");
                    like_button.html("&#10084 Like");
                    $("#"+post_id).prev().find(".like-count").html((count - 1).toString());
                }
            }
        });

    });
});