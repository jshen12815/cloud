$(document).ready(function() {
$("#follow-btn").click(function( event ) {

    form = $(this).parent();
    var url = form.attr("action");

    $.ajax({
        url: url,

        success: function( data ) {

            var button = $(this);
            var count = parseInt(form.prev().html());
            alert(count);
            if (data['followed'] == "True") {
                alert("followed");
                button.removeClass("unfollow-btn");
                button.addClass("follow-btn");
                form.prev.html((count + 1).toString())
            }
            if (data['unfollowed'] == "True") {
                alert("unfollowed");
                button.removeClass("follow-btn");
                button.addClass("unfollow-btn");
                form.prev.html((count - 1).toString())
            }
        }
    });

    return false;
});
});