# Music editing-related actions
import os
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.files import File
from pydub import AudioSegment
from mimetypes import guess_type

from clouddj.forms import *


@login_required
def upload(request):
    if request.method == 'GET':
        form = UploadMusicForm()
    else:
        form = UploadMusicForm(request.POST, request.FILES)
        if form.is_valid():
            new_project = Project(profile=get_object_or_404(Profile, user=request.user), status="in_progress")
            new_project.save()

            song = form.save()
            song.project = new_project
            song.save()
            return render(request, 'edit.html', {'song': song, 'type': get_content_type(song.file.name)})

    render(request, 'upload.html', {'form': form})


@login_required
def save_edit(request, song_id):
    #save latest edit
    song = Song.objects.filter(id=song_id)
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




###################################
### Music Editing Functionality ###
###################################
@login_required
def x_filter(request, song_id):
    song = Song.objects.filter(id=song_id)
    sound = song_to_audioseg(song)

    # handle filtering

    #export new song
    new_song = export_edit(sound, song)
    return render(request, 'edit.html', {'song': new_song, 'type': get_content_type(new_song.file.name)})


########################
### Helper Functions ###
########################
def song_to_audioseg(song):
    filename = song.file.name
    ext = get_ext(filename)

    return AudioSegment.from_file(song.file.path, format=ext[1:])


def export_edit(audio_seg, song):
    new_edit_number = song.edit_number+1
    ext = get_ext(song.file.name)
    root = get_root(song.file.path)
    if song.edit_number > 0:
        root = root.replace("-"+str(song.edit_number), "")
    new_file_path = root + "-" + str(new_edit_number) + ext

    #export song to new file
    audio_seg.export(new_file_path, format=ext[1:])

    #create new file object
    with open(new_file_path, 'w') as f:
        myfile = File(f)

    new_song = Song(file=myfile, edit_number=new_edit_number, project=song.project)
    new_song.save()

    return new_song


def get_content_type(filename):
    return guess_type(filename)[0]


def get_ext(filename):
    return os.path.splitext(filename)[1]


def get_root(filename):
    return os.path.splitext(filename)[0]