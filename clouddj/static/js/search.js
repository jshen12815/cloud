$(document).ready(function() {
$("#tracks-tab").click(function( event ) {


    $(this).parent().addClass("active");
    $("#people-tab").parent().removeClass("active");
    $("#post-block").show();
    return false;
});

$("#people-tab").click(function( event ) {


    $(this).parent().addClass("active");
    $("#tracks-tab").parent().removeClass("active");
    $("#post-block").hide();
    return false;
});
});