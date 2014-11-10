# Music editing-related actions
import os
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.files import File
from pydub import AudioSegment
import pyaudio
import wave
from mimetypes import guess_type
from django.http import HttpResponse, HttpResponseRedirect, Http404

from clouddj.forms import *


def add_empty_forms(context):
    context['filter_form'] = FilterForm()
    context['fade_out_form'] = FadeOutForm()
    context['fade_in_form'] = FadeInForm()
    context['repeat_form'] = RepeatForm()
    context['speedup_form'] = SpeedupForm()
    context['reverse_form'] = ReverseForm()
    context['slice_form'] = SliceForm()


#@login_required
def upload(request):
    if request.method == 'GET':
        form = UploadMusicForm()
    else:
        #new_project = Project(profile=get_object_or_404(Profile, user=request.user), status="in_progress")
        new_project = Project(status="in_progress")
        new_project.save()

        song = Song(project=new_project)

        form = UploadMusicForm(request.POST, request.FILES, instance=song)
        if form.is_valid():
            song = form.save()
            return render(request, 'studio.html', {'song': song, 'type': get_content_type(song.file.name)})

    return render(request, 'upload.html', {'form': form})


#@login_required
def save_edit(request, song_id):
    #save latest edit
    song = Song.objects.get(id=song_id)
    project = song.project
    filepath = list(project.song_set.filter(edit_number=0))[0].file.path
    ext = get_ext(song.file.name)
    audio_seg = song_to_audioseg(song)
    audio_seg.export(filepath, format=ext[1:])

    #create new file object
    with open(filepath, 'w') as f:
        myfile = File(f)

    #delete all temp files - ** user cannot undo edits from a previous session **
    for edit in project.song_set.all():
        os.remove(edit.file.path)
        edit.delete()

    #create new and final song object
    new_song = Song(file=myfile, edit_number=0, project=project)
    new_song.save()

    render(request, 'home.html', {})


"""
@login_required
def record(request):
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if not form.is_valid():
            return
        chunk = 1024
        format = pyaudio.paInt16
        channels = 2
        rate = 44100
        record_seconds = form.cleaned_data['secs']
        wave_output_filename = form.cleaned_data['filename']

        p = pyaudio.PyAudio()

        stream = p.open(format=format,
                        channels=channels,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk)

        print("* recording")

        frames = []

        for i in range(0, int(rate / chunk * record_seconds)):
            data = stream.read(chunk)
            frames.append(data)

        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(wave_output_filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        wf.close()
"""

###################################
### Music Editing Functionality ###
###################################
#@login_required
def x_filter(request, song_id):
    song = Song.objects.get(id=song_id)
    seg = song_to_audioseg(song)
    modified = False

    if request.method == 'POST':
        form = FilterForm(request.POST)
        if not form.is_valid:
            return
        if form.cleaned_data['high_cutoff']:
            modified = True
            seg = seg.high_pass_filter(int(form.cleaned_data['high_cutoff']))
        if form.cleaned_data['low_cutoff']:
            modified = True
            seg = seg.high_pass_filter(int(form.cleaned_data['low_cutoff']))

    #export new song
    if modified:
        new_song = export_edit(seg, song)
    else:
        new_song = song
    return render(request, 'studio.html', {'song': new_song, 'type': get_content_type(new_song.file.name)})


#@login_required
def fade_out(request, song_id):
    song = Song.objects.get(id=song_id)
    seg = song_to_audioseg(song)
    context = {}

    add_empty_forms(context)

    if request.method == 'GET':
        context['song'] = song
        context['type'] = get_content_type(song.file.name)
        return render(request, 'studio.html', context)

    form = FadeOutForm(request.POST)
    context['fade_out_form'] = form
    if not form.is_valid():
        return render(request, 'studio.html', context)

    milliseconds = int(form.seconds)
    new_seg = seg.fade_out(milliseconds * 1000)
    new_song = export_edit(new_seg, song)
    context['song'] = new_song
    context['type'] = get_content_type(song.file.name)

    return render(request, 'studio.html', context)


#@login_required
def fade_in(request, song_id):
    song = Song.objects.get(id=song_id)
    seg = song_to_audioseg(song)
    context = {}

    add_empty_forms(context)

    if request.method == 'GET':
        context['song'] = song
        context['type'] = get_content_type(song.file.name)
        return render(request, 'studio.html', context)

    form = FadeInForm(request.POST)
    context['fade_in_form'] = form
    if not form.is_valid():
        return render(request, 'studio.html', context)

    milliseconds = int(form.seconds)
    new_seg = seg.fade_in(milliseconds * 1000)
    new_song = export_edit(new_seg, song)
    context['song'] = new_song
    context['type'] = get_content_type(song.file.name)

    return render(request, 'studio.html', context)


#@login_required
def repeat(request, song_id):
    song = Song.objects.get(id=song_id)
    seg = song_to_audioseg(song)
    context = {}

    add_empty_forms(context)

    if request.method == 'GET':
        context['song'] = song
        context['type'] = get_content_type(song.file.name)
        return render(request, 'studio.html', context)

    form = RepeatForm(request.POST)
    context['repeat_form'] = form
    if not form.is_valid():
        return render(request, 'studio.html', context)

    start = int(form.start)
    end = int(form.end)
    iters = int(form.iters)

    lower_seg = seg[:start]
    upper_seg = seg[-end:]
    middle_seg = seg[start:end]

    new_seg = lower_seg + middle_seg*iters + upper_seg
    new_song = export_edit(new_seg, song)
    context['song'] = new_song
    context['type'] = get_content_type(song.file.name)

    return render(request, 'studio.html', context)


#@login_required
def speedup(request, song_id):
    song = Song.objects.get(id=song_id)
    seg = song_to_audioseg(song)
    context = {}

    add_empty_forms(context)

    if request.method == 'GET':
        context['song'] = song
        context['type'] = get_content_type(song.file.name)
        return render(request, 'studio.html', context)

    form = SpeedupForm(request.POST)
    context['speedup_form'] = form
    if not form.is_valid():
        return render(request, 'studio.html', context)

    changed = seg.speedup(form.cleaned_data['multiplier'])

    new_song = export_edit(changed, song)
    context['song'] = new_song
    context['type'] = get_content_type(song.file.name)

    return render(request, 'studio.html', context)


#@login_required
def reverse(request, song_id):
    song = Song.objects.get(id=song_id)
    seg = song_to_audioseg(song)
    context = {}

    add_empty_forms(context)

    if request.method == 'GET':
        context['song'] = song
        context['type'] = get_content_type(song.file.name)
        return render(request, 'studio.html', context)

    form = ReverseForm(request.POST)
    context['reverse_form'] = form
    if not form.is_valid():
        return render(request, 'studio.html', context)

    start = int(form.cleaned_data['start'])
    end = int(form.cleaned_data['end'])

    lower_seg = seg[:start]
    upper_seg = seg[-end:]
    middle_seg = seg[start:end]

    new_seg = lower_seg + middle_seg.reverse() + upper_seg
    new_song = export_edit(new_seg, song)
    context['song'] = new_song
    context['type'] = get_content_type(song.file.name)

    return render(request, 'studio.html', context)


#@login_required
def slice(request, song_id):
    song = Song.objects.get(id=song_id)
    seg = song_to_audioseg(song)
    context = {}

    add_empty_forms(context)

    if request.method == 'GET':
        context['song'] = song
        context['type'] = get_content_type(song.file.name)
        return render(request, 'studio.html', context)

    form = ReverseForm(request.POST)
    context['slice_form'] = form
    if not form.is_valid():
        return render(request, 'studio.html', context)

    start = int(form.cleaned_data['start'])
    end = int(form.cleaned_data['end'])

    lower_seg = seg[:start]
    upper_seg = seg[-end:]

    new_seg = lower_seg + upper_seg
    new_song = export_edit(new_seg, song)
    context['song'] = new_song
    context['type'] = get_content_type(song.file.name)

    return render(request, 'studio.html', context)


########################
### Helper Functions ###
########################
#@login_required
def get_song(request, id):
    song = get_object_or_404(Song, id=id)
    if not song.file:
        raise Http404
        
    content_type = guess_type(song.file.name)
    return HttpResponse(song.file, content_type=content_type)

def song_to_audioseg(song):
    filename = song.file.name
    ext = get_ext(filename)

    return AudioSegment.from_file(song.file.path, format=ext[1:])


def export_edit(audio_seg, old_song):
    new_edit_number = old_song.edit_number+1
    ext = get_ext(old_song.file.name)
    root = get_root(old_song.file.path)
    if old_song.edit_number > 0:
        root = root.replace("-"+str(old_song.edit_number), "")
    new_file_path = root + "-" + str(new_edit_number) + ext

    #export song to new file
    audio_seg.export(new_file_path, format=ext[1:])

    #create new file object
    with open(new_file_path, 'w') as f:
        myfile = File(f)

    new_song = Song(file=myfile, edit_number=new_edit_number, project=old_song.project)
    new_song.save()

    return new_song


def get_content_type(filename):
    return guess_type(filename)[0]


def get_ext(filename):
    return os.path.splitext(filename)[1]


def get_root(filename):
    return os.path.splitext(filename)[0]