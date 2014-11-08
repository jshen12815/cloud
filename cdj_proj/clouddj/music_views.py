# Music editing-related actions
from django.shortcuts import render

from clouddj.models import *
from clouddj.forms import *


def upload(request):
    if request.method == 'GET':
        form = UploadMusicForm()
    else:
        form = UploadMusicForm(request.POST, request.FILES)
        if form.is_valid():
            return render(request, 'edit.html', {})

    render(request, 'upload.html', {'form': form})