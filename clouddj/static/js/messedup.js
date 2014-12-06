



$(document).ready(function() {

$(".starrate").click(function( event ) {
  var form = $(".rateform");
  var url = $(this).parent().attr("href");
  var csrf_name = form.find("[type=hidden]").attr("name");
  var rating = $(this);
   alert("nooo");

    $.ajax({
        url: url,

        data: {
            "csrfmiddlewaretoken": $("#csrf").val()
        },

        type: "POST",

        success: function( data ) {
            alert("yay");
            var rating = data['rating'];
            var post_id = data ['post_id'];
            //var num_ratings = parseInt($("#"+post_id).parent().parent().prev().find(".numratings").html());
            var count=$("#"+post_id).parent().parent().prev().find(".user-rating").html();
            alert(count);
            //var stars = parseInt($("#"+post_id).parent().parent().prev().find(".starrate").html());



            //if data my rating exists then dont update num ratings, update myrating then stars

            
        }
    });

    return false;
});
});

