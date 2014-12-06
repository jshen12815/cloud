$(document).ready(function() {
$(".fu-btn").click(function( event ) {

    form = $(this).parent();
    var url = form.attr("action");
    var button = $(this);

    $.ajax({
        url: url,

        success: function( data ) {

            var count = parseInt(form.prev().html());
            if (data['followed'] == "True") {
                button.addClass("unfollow-btn");
                button.removeClass("follow-btn");
                button.find(".btn-text").html("Unfollow");
                form.prev().html((count + 1).toString());
            }
            if (data['unfollowed'] == "True") {
                button.addClass("follow-btn");
                button.removeClass("unfollow-btn");
                button.find(".btn-text").html("Follow");
                form.prev().html((count - 1).toString());
            }
        }
    });

    return false;
});
});