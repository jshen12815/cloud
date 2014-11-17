var wavesurfer = Object.create(WaveSurfer);

/**
 * Init & load.
 */
document.addEventListener('DOMContentLoaded', function () {
    // Init wavesurfer
    wavesurfer.init({
        container: '#waveform',
        height: 100,
        scrollParent: true,
        normalize: true,
        minimap: true,
        backend: 'AudioElement'
    });
    
    var src = $("#audio_src").attr("src");
    wavesurfer.load(src);



    /* Regions */
    wavesurfer.enableDragSelection({
        color: "rgba(0, 0, 0, 0.1)"
    });

    wavesurfer.on('region-click', function (region, e) {
        e.stopPropagation();
        // Play on click, loop on shift click
        e.shiftKey ? region.playLoop() : region.play();
    });
    
    wavesurfer.on('region-created', deleteOldRegion);

    wavesurfer.on('region-play', function (region) {
        region.once('out', function () {
            wavesurfer.play(region.start);
            wavesurfer.pause();
        });
    });


    /* Minimap plugin */
    wavesurfer.initMinimap({
        height: 30,
        waveColor: '#ddd',
        progressColor: '#999',
        cursorColor: '#999'
    });


    /* Timeline plugin */
    wavesurfer.on('ready', function () {
        var timeline = Object.create(WaveSurfer.Timeline);
        timeline.init({
            wavesurfer: wavesurfer,
            container: "#wave-timeline"
        });
    });


    /* Toggle play/pause buttons. */
    var playButton = document.querySelector('#play');
    var pauseButton = document.querySelector('#pause');
    wavesurfer.on('play', function () {
        playButton.style.display = 'none';
        pauseButton.style.display = '';
    });
    wavesurfer.on('pause', function () {
        playButton.style.display = '';
        pauseButton.style.display = 'none';
    });
});

function deleteOldRegion(Region){
    var regions = wavesurfer.regions.list;
    $.each(regions, function(index, value){
        if (value != Region) {
            value.remove();
        }
    });
}

//when user submits edit form
function getTime(){
    var regions = wavesurfer.regions.list;
    if (regions) {
        var region = regions[0];
        var start_sec = region.start;
        var end_sec = region.end;
    }

}
