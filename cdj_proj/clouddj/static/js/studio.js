window.AudioContext = window.AudioContext || window.webkitAudioContext;

var needsConfirmation = true;
var audioContext = new AudioContext();
var audioInput = null,
    realAudioInput = null,
    inputPoint = null,
    audioRecorder = null;

$(".music_form").submit(function (event) {
    var form = $(this);
    var postData = $(this).serializeArray();
    var formURL = $(this).attr("action");
    $.ajax(
        {
            url: formURL,
            type: "POST",
            data: postData,
            success: function(data){
                console.log(data);
                updatePage(data);
                form.find("input[type=text], textarea").val("");
            }
        });
    return false;
});

function toggleRecording(e) {
    if (e.classList.contains("recording")) {
        // stop recording
        audioRecorder.stop();
        e.classList.remove("recording");
        audioRecorder.exportWAV(handleRecording);
    } else {
        // start recording
        if (!audioRecorder)
            return;
        e.classList.add("recording");
        audioRecorder.clear();
        audioRecorder.record();
    }
}

function handleRecording(blob) {
    var form = $("#record_form");
    var url = form.attr("action");
    var inputs = form.find(":input");
    var fd = new FormData();

    inputs.each(function () {
        fd.append($(this).attr("name"), $(this).val());
    });
    fd.append('recording', blob);

    $.ajax({
        type: 'POST',
        url: url,
        data: fd,
        processData: false,
        contentType: false,
        success: function(data){
                updatePage(data);
                form.find("input[type=text], textarea").val("");
            }
    });
}
function reloadSong(){
    document.getElementById("audio_controls").load();
}
function updatePage(data) {
    //reload song
    //reload song
    var audio = $("#audio_src");
    audio.attr("type", data['type']);
    var new_src = audio.attr("src").replace(/\d+/, data['song_id']);
    audio.attr("src", new_src);
    reloadSong();

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

function gotStream(stream) {
    inputPoint = audioContext.createGain();

    // Create an AudioNode from the stream.
    realAudioInput = audioContext.createMediaStreamSource(stream);
    audioInput = realAudioInput;
    audioInput.connect(inputPoint);

//    audioInput = convertToMono( input );

    analyserNode = audioContext.createAnalyser();
    analyserNode.fftSize = 2048;
    inputPoint.connect(analyserNode);

    audioRecorder = new Recorder(inputPoint);

    zeroGain = audioContext.createGain();
    zeroGain.gain.value = 0.0;
    inputPoint.connect(zeroGain);
    zeroGain.connect(audioContext.destination);
}

function initAudio() {
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
            alert('Error getting audio');
            console.log(e);
        });
}

function confirmExit(){
    if (needsConfirmation){
        return "You have not saved! If you made any changes they will be lost."
    }
}

window.addEventListener('load', initAudio);
window.onbeforeunload = confirmExit;