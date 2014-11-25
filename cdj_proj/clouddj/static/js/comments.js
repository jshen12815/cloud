$(document).ready(function() {
$(".comm-form").submit(function( event ) {

    var form = $(this);
    var url = form.attr("action");
    var csrf_name = form.find("[type=hidden]").attr("name");

    $.ajax({
        url: url,

        data: {
            "comm": form.find("[type=text]").val(),
            "csrfmiddlewaretoken": $("#csrf").val()
        },

        type: "POST",

        success: function( data ) {
            form.find("[type=text]").val('');
            var count = parseInt(form.parent().next().find("[data-toggle=collapse]").html());
            form.parent().next().find("[data-toggle=collapse]").html((count + 1).toString());
            var comment = data['comment'];
            var username = data['username'];
            var user_id = data['user_id'];
            var post_id = data['post_id'];
            //$("#"+post_id).addClass("in");
            $("#"+post_id).append("\
                                  <div class='row'>\
                                    <div class='col-md-1'>\
                                        <a style='color: black'>\
                                            <h2 class='panel-title comment-username'><b>"+username+"</b></h2>\
                                        </a>\
                                        <div style='width:200px'>\
                                            <p class='comment-text'>"+comment+"</p>\
                                        </div>\
                                    </div>\
                                  </div>\
                                ");
        }
    });

    return false;
});
});