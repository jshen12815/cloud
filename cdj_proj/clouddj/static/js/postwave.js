'use strict';

// Create an instance
var wavesurfer = Object.create(WaveSurfer);

// Init & load audio file
document.addEventListener('DOMContentLoaded', function () {
    var options = {
        container     : document.querySelector('#waveform'),
        waveColor     : 'dimgray',
        progressColor : '#6FE1D5',
        loaderColor   : 'purple',
        cursorColor   : 'navy',
        notchPercentHeight : 50
    };

    if (location.search.match('scroll')) {
        options.minPxPerSec = 20;
        options.scrollParent = true;
    }

    if (location.search.match('normalize')) {
        options.normalize = true;
    }

    // Init
    wavesurfer.init(options);
    // Load audio from URL
    //get elementbyidx
    var src = $("#audio_src").attr("src");
    wavesurfer.load(src);


   
});


// Report errors
wavesurfer.on('error', function (err) {
    console.error(err);
});


/* Progress bar */
document.addEventListener('DOMContentLoaded', function () {
    var progressDiv = document.querySelector('#progress-bar');
    var progressBar = progressDiv.querySelector('.progress-bar');

    var showProgress = function (percent) {
        progressDiv.style.display = 'block';
        progressBar.style.width = percent + '%';
    };

    var hideProgress = function () {
        progressDiv.style.display = 'none';
    };

    wavesurfer.on('loading', showProgress);
    wavesurfer.on('ready', hideProgress);
    wavesurfer.on('destroy', hideProgress);
    wavesurfer.on('error', hideProgress);
});

var GLOBAL_ACTIONS = {
    'play': function () {
        wavesurfer.playPause();
    },

    'back': function () {
        wavesurfer.skipBackward();
    },

    'forth': function () {
        wavesurfer.skipForward();
    },

    'toggle-mute': function () {
        wavesurfer.toggleMute();
    }
};


// Bind actions to buttons and keypresses
document.addEventListener('DOMContentLoaded', function () {
   
    [].forEach.call(document.querySelectorAll('[data-action]'), function (el) {
        el.addEventListener('click', function (e) {
            var action = e.currentTarget.dataset.action;
            if (action in GLOBAL_ACTIONS) {
                e.preventDefault();
                GLOBAL_ACTIONS[action](e);
            }
        });
    });
});




