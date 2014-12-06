$(document).ready(function() {
$("#tracks-tab").click(function( event ) {


    $(this).parent().addClass("active");
    $("#people-tab").parent().removeClass("active");
    $("#post-block").show();
    $("#post-count").show();
    $("#users-block").attr('style','display:none');
    return false;
});

$("#people-tab").click(function( event ) {


    $(this).parent().addClass("active");
    $("#tracks-tab").parent().removeClass("active");
    $("#post-block").hide();
    $("#post-count").hide();
    $("#users-block").removeAttr("style");
    return false;
});
});