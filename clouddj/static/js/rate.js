



$(document).ready(function() {

$(".starrate").click(function( event ) {
  var form = $(".rateform");
  var url = $(this).parent().parent().prev();
  var csrf_name = form.find("[type=hidden]").attr("name");
  var rating = parseInt($(this).val());
  console.log(rating);

    $.ajax({
        url: url,

        data: {
            "csrfmiddlewaretoken": $("#csrf").val(),
            "rating" : rating
        },

        type: "POST",

        success: function( data ) {
            alert("yay");
            var rating = data['rating'];
            var post_id = data ['post_id'];
            var count=$("#"+post_id).parent().parent().prev().find(".user-rating").html(rating);
            alert("count");
            
            
        }
    });

    return false;
});
});

