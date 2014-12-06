$(document).ready(function() {
    $("li").on("click", function() {
        var sel = $(this).attr("sel");
        $(".tab-content").children().removeClass("active");
        $(sel).addClass("active");
    });
});