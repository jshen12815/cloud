window.AudioContext = window.AudioContext || window.webkitAudioContext;

var song_id, ol;
var needsConfirmation = false;
var audioContext = new AudioContext();
var wavesurfer_mic = Object.create(WaveSurfer);
var microphone = null;
var audioInput = null,
    realAudioInput = null,
    inputPoint = null,
    audioRecorder = null;

/* handle forms */
$(".slider-input").change(function (event) {
    var form = $(this).parent();
    form.submit();
});

$(".music_form").submit(function (event) {
    var form = $(this);
    var inputs = form.find(":input");
    var formURL = form.attr("action");
    var regions = wavesurfer.regions.list;
    var fd = new FormData();
    var start, end;

    inputs.each(function () {
        fd.append($(this).attr("name"), $(this).val());
    });

    if (!isEmpty(regions)) {
        Object.keys(regions).map(function (id) {
            var region = regions[id];
            start = region.start;
            end = region.end;
        });
    } else {
        start = 0;
        end = wavesurfer.getDuration();
    }

    if (formURL.indexOf('fade') >= 0) {
        start = Math.round(start);
        end = Math.round(end);
    }

    fd.append('start', start);
    fd.append('end', end);

    $.ajax(
        {
            url: formURL,
            type: "POST",
            data: fd,
            processData: false,
            contentType: false,
            success: function (data) {
                needsConfirmation = true;
                updatePage(data);
                form.find("input[type=text], textarea").val("");
                var el = $(".slider-input");
                el.val(el.data('oldVal'));
            }
        });
    return false;
});

function toggleRecording(e) {
    if (e.classList.contains("recording")) {
        // stop recording
        audioRecorder.stop();
        $("#waveform-mic").hide();
        microphone.levelChecker.disconnect();
        microphone.wavesurfer.empty();
        e.classList.remove("recording");
        audioRecorder.exportWAV(handleRecording);
    } else {
        // start recording
        if (!audioRecorder)
            return;
        e.classList.add("recording");
        $("#waveform-mic").show();
        microphone.levelChecker = audioContext.createScriptProcessor(4096, 1, 1);
        microphone.mediaStreamSource.connect(microphone.levelChecker);
        microphone.levelChecker.connect(audioContext.destination);
        microphone.levelChecker.onaudioprocess = microphone.reloadBuffer.bind(microphone);
        audioRecorder.clear();
        audioRecorder.record();
    }
}

function handleRecording(blob) {
    var form = $("#record_form");
    var url = form.attr("action");
    var inputs = form.find(":input");
    var regions = wavesurfer.regions.list;
    var fd = new FormData();
    var start;

    inputs.each(function () {
        fd.append($(this).attr("name"), $(this).val());
    });

    if (!isEmpty(regions)) {
        Object.keys(regions).map(function (id) {
            var region = regions[id];
            start = region.start;
        });
    } else {
        start = wavesurfer.getCurrentTime();
    }

    fd.append('start', start);
    fd.append('recording', blob);

    $.ajax({
        type: 'POST',
        url: url,
        data: fd,
        processData: false,
        contentType: false,
        success: function (data) {
            needsConfirmation = true;
            updatePage(data);
            form.find("input[type=text], textarea").val("");
        }
    });
}

function updatePage(data) {
    //reload song
    song_id = data['song_id']; //used to discard changes
    var audio = $("#audio_src");
    var new_src = audio.attr("src").replace(/\d+/, data['song_id']);
    audio.attr("src", new_src);

    $("#wave-timeline").empty();
    wavesurfer.load(new_src);


    var body = $('body');
    var edit_forms = body.find(".music_form");
    edit_forms.each(function (index, item) {
        var form = $(this);
        var action = form.attr("action");
        var new_action = action.replace(/\d+/, data['song_id']);
        form.attr("action", new_action);
    });

    var control_forms = body.find(".control_form");
    control_forms.each(function (index, item) {
        var form = $(this);
        var action = form.attr("action");
        var new_action = action.replace(/\d+/, data['song_id']);
        form.attr("action", new_action);
    });
}

/* set up recording and microphone waveform */
function gotStream(stream) {
    //setup mic
    microphone.stream = stream;
    microphone.active = true;


    inputPoint = audioContext.createGain();

    // Create an AudioNode from the stream.
    realAudioInput = audioContext.createMediaStreamSource(stream);
    microphone.mediaStreamSource = realAudioInput;
    audioInput = realAudioInput;
    audioInput.connect(inputPoint);

//    audioInput = convertToMono( input );

    analyserNode = audioContext.createAnalyser();
    analyserNode.fftSize = 2048;
    inputPoint.connect(analyserNode);

    audioRecorder = new Recorder(inputPoint, {'workerPath':'recorderJs/recorderWorker.js');

    zeroGain = audioContext.createGain();
    zeroGain.gain.value = 0.0;
    inputPoint.connect(zeroGain);
    zeroGain.connect(audioContext.destination);
}

function initAudio() {
    var el = $(".slider-input");
    el.data('oldVal',  el.val() );
    if (!navigator.getUserMedia)
        navigator.getUserMedia = navigator.webkitGetUserMedia || navigator.mozGetUserMedia;
    if (!navigator.cancelAnimationFrame)
        navigator.cancelAnimationFrame = navigator.webkitCancelAnimationFrame || navigator.mozCancelAnimationFrame;
    if (!navigator.requestAnimationFrame)
        navigator.requestAnimationFrame = navigator.webkitRequestAnimationFrame || navigator.mozRequestAnimationFrame;

    navigator.getUserMedia(
        {
            "audio": {
                "mandatory": {
                    "googEchoCancellation": "false",
                    "googAutoGainControl": "false",
                    "googNoiseSuppression": "false",
                    "googHighpassFilter": "false"
                },
                "optional": []
            }
        }, gotStream, function (e) {
            console.log(e);
        });

    wavesurfer_mic.init({
        container: '#waveform-mic',
        waveColor: 'dimgray',
        loopSelection: false,
        cursorWidth: 0,
        height: $("#record").height()
    });

    microphone = Object.create(WaveSurfer.Microphone);

    microphone.init({
        wavesurfer: wavesurfer_mic
    });
}

/* handle user navigation and edits */
function confirmExit() {
    if (needsConfirmation) {
        return "You have unsaved changes! Your changes will be lost unless you save them. "
    }
}

function discardChanges() {
    //only true when changes have been made
    if (needsConfirmation) {
        var url = '/clouddj/undo_all/' + song_id + '/';
        var csrf_token = $("input[name=csrfmiddlewaretoken]").val();
        $.ajax(
            {
                url: url,
                type: "POST",
                data: {"csrfmiddlewaretoken": csrf_token},
                async: false
            }
        )
    }
}

window.addEventListener('load', initAudio);
window.onbeforeunload = confirmExit;
window.addEventListener('unload', discardChanges);


/* Posting */

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

/* helper functions */
function isEmpty(map) {
    for (var key in map) {
        if (map.hasOwnProperty(key)) {
            return false;
        }
    }
    return true;
}

$(".help-btn").tooltip({
    html: true,
    placement: "bottom",
    title: function() {
        return "<ul><li>Click and drag to select region of song</li><li>Click on region to play it</li><li>Shift + Click to loop play</li><li>Ctrl + Click to delete region</li></ul>";
    }
});