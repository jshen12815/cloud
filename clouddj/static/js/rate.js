



$(document).ready(function() {

$(".starrate").click(function( event ) {
  var form = $(".rateform");
  var url = $(this).parent().attr("href");
  var csrf_name = form.find("[type=hidden]").attr("name");
  var rating = $(this);
  

    $.ajax({
        url: url,

        data: {
            "csrfmiddlewaretoken": $("#csrf").val()
        },

        type: "POST",

        success: function( data ) {
            var post_id = data ['post_id'];
            var num_ratings = parseInt($("#"+post_id).parent().parent().prev().find(".numratings").html());
            var my_rating = parseInt($("#"+post_id).parent().parent().prev().find(".user-rating").html());
            var stars = parseInt($("#"+post_id).parent().parent().prev().find(".starrate").html());

            if (data['liked'] == "True") {
                like_button.addClass("lit-like");
                like_button.html("&#10084 Unlike");
                $("#"+post_id).parent().parent().prev().find(".like-count").html((count + 1).toString());
            }

            //if data my rating exists then dont update num ratings, update myrating then stars

            console.log ( '#sweeeet' );
            
        }
    });

    return false;
});
});

