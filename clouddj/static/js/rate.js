 /*
 $(document).ready(function() { 
    console.log("hellooo");
    var url = $(this).parent().attr("href");
     {
          form.submit();

   });
  });
*/





$(document).ready(function() {
$(".starrate").click(function( event ) {
    var url = "a"//$(this).parent().attr("url");
    //var csrf_name = form.find("[type=hidden]").attr("name");

    console.log($(this).parent().attr("post-id"));


    $.ajax({
        url: url,

        data: {
            "csrfmiddlewaretoken": $("#csrf").val()
        },

        type: "POST",

        success: function( data ) {
            
            
        }
    });

    return false;
});
});