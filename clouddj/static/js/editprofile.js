$(document).ready(function() {
$('#file-input').change(function () {
    var imageFile = document.getElementById('file-input').files[0];
    var reader = new FileReader();
    reader.readAsDataURL(imageFile);
    reader.onloadend = function (e) {
        var image = $('<img>');
        image.error(function () {
            $(this).remove();
        }).attr('src', e.target.result);
        image.addClass('img-rounded modal-photo');
        var images = $('#images');
        if (images.children().length != 0) {
            images.empty();
        }
        $(image).appendTo('#images');
    };
});
});