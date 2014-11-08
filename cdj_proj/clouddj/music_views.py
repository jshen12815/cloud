# Music editing-related actions
from django.shortcuts import render
from pydub import AudioSegment
from mimetypes import guess_type

from clouddj.models import *
from clouddj.forms import *


def upload(request):
    if request.method == 'GET':
        form = UploadMusicForm()
    else:
        form = UploadMusicForm(request.POST, request.FILES)
        if form.is_valid():
            song = form.save()
            content_type = guess_type(song.file.name)
            return render(request, 'edit.html', {'file': song.file, 'type': content_type})

    render(request, 'upload.html', {'form': form})