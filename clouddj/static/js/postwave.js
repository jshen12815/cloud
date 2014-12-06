'use strict';


document.addEventListener('DOMContentLoaded', function () {

    var waves = $(".waveform");

    waves.each(function(index, element) {
        var id = $(this).attr("id").match(/\d+/)[0];

        var options = {
        container     : element,
        //scrollParent  : true,
        waveColor     : 'dimgray',
        progressColor : '#6FE1D5',
        loaderColor   : 'purple',
        cursorColor   : 'navy',
        height        : 100
        };

        if (location.search.match('scroll')) {
            options.minPxPerSec = 100;
            options.scrollParent = true;
        }

        if (location.search.match('normalize')) {
            options.normalize = true;
        }


        var wave = Object.create(WaveSurfer);
        wave.init(options);
        var src = $("#audiosrc-"+id).attr("src");
        wave.load(src);

        // Report errors
        wave.on('error', function (err) {
            console.error(err);
        });

        /* Progress bar */
        var progressDiv = document.querySelector('#progressbar-'+id);
        var progressBar = progressDiv.querySelector('.progress-bar');

        var showProgress = function (percent) {
            progressDiv.style.display = 'block';
            progressBar.style.width = percent + '%';
        };

        var hideProgress = function () {
            progressDiv.style.display = 'none';
        };

        wave.on('loading', showProgress);
        wave.on('ready', hideProgress);
        wave.on('destroy', hideProgress);
        wave.on('error', hideProgress);

        $("#play-"+id).click(function(){
            wave.playPause();
        });
    });
   
});








