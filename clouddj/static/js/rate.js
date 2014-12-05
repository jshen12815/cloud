 
 $(document).ready(function() { 
    console.log("hellooo");
    var url = $(this).parent().attr("href");
     {
          form.submit();

   });
  });



/*



$(".starrate").click(function( event ) {
   // var url = "a"//$(this).parent().attr("url");
    //var csrf_name = form.find("[type=hidden]").attr("name");

    //console.log($(this).parent().attr("post-id"));


 //   $.ajax({//
   //     url: url,

   // $(".starrate").click(function( event ) {

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
            
            
        }
    });


    });
});*/