# Music editing-related actions
import os
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.files import File
from pydub import *
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
    context['amplify_form'] = AmplifyForm()
    context['search_form'] = SearchForm()


@login_required
def upload(request):
    if request.method == 'GET':
        form = UploadMusicForm()
    else:
        new_project = Project(profile=get_object_or_404(Profile, user=request.user), status="in_progress")
        # new_project = Project(status="in_progress")
        new_project.save()

        song = Song(project=new_project)

        form = UploadMusicForm(request.POST, request.FILES, instance=song)
        if form.is_valid():
            song = form.save()
            #name = get_root(song.file.name).replace("music/", "")
            song.name = request.POST['name']
            song.save()
            return redirect('/clouddj/studio')

    return render(request, 'upload.html', {'form': form, 'user': request.user})


@login_required
def studio(request, proj_id=None):
    profile = get_object_or_404(Profile, user=request.user)
    projects = Project.objects.filter(profile=profile, status="in_progress").order_by("-id")
    if not projects:
        return redirect('/clouddj/upload')
    if proj_id:
        proj = get_object_or_404(Project, id=proj_id)
    else:
        proj = projects[0]

    song = get_object_or_404(Song, edit_number=0, project=proj)

    # remove unsaved changes
    if len(proj.song_set.all()) > 1:
        undo_all(request, song.id)

    #name = get_root(song.file.name).replace("music/", "")
    #song.name = name
    context = {'song': song, 'type': get_content_type(song.file.name), 'user': request.user, 'projects': projects}
    add_empty_forms(context)
    return render(request, 'studio.html', context)


@login_required
def save_song(request, song_id):
    # save latest edit to original file
    song = get_object_or_404(Song, id=song_id)
    project = song.project
    final_song = get_object_or_404(Song, edit_number=0, project=project)
    ext = get_ext(final_song.file.name)
    audio_seg = song_to_audioseg(song)
    f = audio_seg.export(final_song.file.path, format=ext[1:])
    f.close()

    #delete all temp files - ** user cannot undo edits from a previous session **
    undo_all(request, song_id)

    return redirect('/clouddj/studio/' + str(project.id))


@login_required
def undo_all(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    project = song.project
    final_song = get_object_or_404(Song, edit_number=0, project=project)

    # delete all temp files
    all_edits = project.song_set.all()
    for edit in all_edits:
        if not final_song == edit:
            if os.path.isfile(edit.file.path):
                os.remove(edit.file.path)
            edit.delete()


@login_required
def delete(request, song_id):
    undo_all(request, song_id)
    song = get_object_or_404(Song, id=song_id)
    song.project.delete()
    if os.path.isfile(song.file.path):
        os.remove(song.file.path)
    song.delete()
    return redirect('/clouddj/studio')

# ##################################
### Music Editing Functionality ###
###################################
@login_required
def record(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    response_text = {'type': get_content_type(song.file.name), 'song_id': str(song.id)}

    if request.method == 'GET':
        return HttpResponse(json.dumps(response_text), content_type="application/json")

    form = RecordForm(request.POST)
    if not form.is_valid():
        return HttpResponse(json.dumps(response_text), content_type="application/json")

    temp_file = request.FILES['recording']
    seg = song_to_audioseg(song)
    recording = AudioSegment.from_file(temp_file, format='wav')
    start_time = float(form.cleaned_data['start'])
    start_time *= 1000

    if start_time / 1000 >= len(seg) / 1000:
        # append
        silent_secs = start_time - len(seg)
        silence = AudioSegment.silent(duration=silent_secs)
        seg = seg + silence + recording
    else:
        seg = seg.overlay(recording, start_time)
        if len(recording) > len(seg):
            remaining = len(recording) - len(seg)
            seg += recording[remaining:]

    new_song = export_edit(seg, song)
    response_text = {'type': get_content_type(new_song.file.name), 'song_id': str(new_song.id)}

    return HttpResponse(json.dumps(response_text), content_type="application/json")


@login_required
def undo(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    previous_edit = song.edit_number - 1
    response_text = {'type': get_content_type(song.file.name), 'song_id': str(song.id)}

    if len(list(song.project.song_set.all())) <= 1:
        return HttpResponse(json.dumps(response_text), content_type="application/json")

    new_song = get_object_or_404(Song, edit_number=previous_edit, project=song.project)

    #delete undone edit
    os.remove(song.file.path)
    song.delete()

    response_text = {'type': get_content_type(new_song.file.name), 'song_id': str(new_song.id)}

    return HttpResponse(json.dumps(response_text), content_type="application/json")


@login_required
def x_filter(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    seg = song_to_audioseg(song)
    response_text = {'type': get_content_type(song.file.name), 'song_id': str(song.id)}

    if request.method == 'GET':
        return HttpResponse(json.dumps(response_text), content_type="application/json")

    form = FilterForm(request.POST)

    if not form.is_valid():
        return HttpResponse(json.dumps(response_text), content_type="application/json")

    start = float(form.cleaned_data['start']) * 1000
    end = float(form.cleaned_data['end']) * 1000
    high_cut = form.cleaned_data['high_cutoff']
    low_cut = form.cleaned_data['low_cutoff']

    if start and end:
        lower_seg = seg[:start]
        upper_seg = seg[end:]
        middle_seg = seg[start:end]

        if high_cut:
            middle_seg = middle_seg.high_pass_filter(float(high_cut))
        if low_cut:
            middle_seg = middle_seg.low_pass_filter(float(low_cut))

        seg = lower_seg + middle_seg + upper_seg
    else:
        if high_cut:
            seg = seg.high_pass_filter(float(high_cut))
        if low_cut:
            seg = seg.low_pass_filter(float(low_cut))

    #export new song
    new_song = export_edit(seg, song)

    response_text = {'type': get_content_type(new_song.file.name), 'song_id': str(new_song.id)}

    return HttpResponse(json.dumps(response_text), content_type="application/json")


@login_required
def fade_out(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    seg = song_to_audioseg(song)
    response_text = {'type': get_content_type(song.file.name), 'song_id': str(song.id)}

    if request.method == 'GET':
        return HttpResponse(json.dumps(response_text), content_type="application/json")

    form = FadeOutForm(request.POST)

    if not form.is_valid():
        return HttpResponse(json.dumps(response_text), content_type="application/json")

    milliseconds = int(form.cleaned_data['end']) - int(form.cleaned_data['start'])
    new_seg = seg.fade_out(milliseconds * 1000)
    new_song = export_edit(new_seg, song)
    response_text = {'type': get_content_type(new_song.file.name), 'song_id': str(new_song.id)}

    return HttpResponse(json.dumps(response_text), content_type="application/json")


@login_required
def fade_in(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    seg = song_to_audioseg(song)
    response_text = {'type': get_content_type(song.file.name), 'song_id': str(song.id)}

    if request.method == 'GET':
        return HttpResponse(json.dumps(response_text), content_type="application/json")

    form = FadeInForm(request.POST)

    if not form.is_valid():
        return HttpResponse(json.dumps(response_text), content_type="application/json")

    milliseconds = int(form.cleaned_data['end']) - int(form.cleaned_data['start'])
    new_seg = seg.fade_in(milliseconds * 1000)
    new_song = export_edit(new_seg, song)
    response_text = {'type': get_content_type(new_song.file.name), 'song_id': str(new_song.id)}

    return HttpResponse(json.dumps(response_text), content_type="application/json")


@login_required
def repeat(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    seg = song_to_audioseg(song)
    response_text = {'type': get_content_type(song.file.name), 'song_id': str(song.id)}

    if request.method == 'GET':
        return HttpResponse(json.dumps(response_text), content_type="application/json")

    form = RepeatForm(request.POST)

    if not form.is_valid():
        return HttpResponse(json.dumps(response_text), content_type="application/json")

    start = float(form.cleaned_data['start']) * 1000
    end = float(form.cleaned_data['end']) * 1000
    iters = int(form.cleaned_data['iters'])

    lower_seg = seg[:start]
    upper_seg = seg[end:]
    middle_seg = seg[start:end]

    new_seg = lower_seg + middle_seg * iters + upper_seg
    new_song = export_edit(new_seg, song)
    response_text = {'type': get_content_type(new_song.file.name), 'song_id': str(new_song.id)}

    return HttpResponse(json.dumps(response_text), content_type="application/json")


@login_required
def tempo(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    seg = song_to_audioseg(song)
    response_text = {'type': get_content_type(song.file.name), 'song_id': str(song.id)}

    if request.method == 'GET':
        return HttpResponse(json.dumps(response_text), content_type="application/json")

    form = SpeedupForm(request.POST)

    if not form.is_valid():
        print form.errors
        return HttpResponse(json.dumps(response_text), content_type="application/json")

    print form.cleaned_data['multiplier']
    changed = seg.speedup(form.cleaned_data['multiplier'], crossfade=0)

    new_song = export_edit(changed, song)
    response_text = {'type': get_content_type(new_song.file.name), 'song_id': str(new_song.id)}

    return HttpResponse(json.dumps(response_text), content_type="application/json")


@login_required
def bass(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    seg = song_to_audioseg(song)
    response_text = {'type': get_content_type(song.file.name), 'song_id': str(song.id)}

    if request.method == 'GET':
        return HttpResponse(json.dumps(response_text), content_type="application/json")

    form = AmplifyForm(request.POST)

    if not form.is_valid():
        return HttpResponse(json.dumps(response_text), content_type="application/json")

    start = float(form.cleaned_data['start']) * 1000
    end = float(form.cleaned_data['end']) * 1000
    amp = int(form.cleaned_data['amplify'])

    lower_seg = seg[:start]
    upper_seg = seg[end:]
    middle_seg = seg[start:end]

    middle_bass = middle_seg.low_pass_filter(140)
    middle_bass = middle_bass.high_pass_filter(20)

    modify = -1 if amp > 0 else 1
    middle_bass = middle_bass.apply_gain(amp+modify)

    middle_seg = middle_seg.overlay(middle_bass)

    seg = lower_seg + middle_seg + upper_seg

    #export new song
    new_song = export_edit(seg, song)

    response_text = {'type': get_content_type(new_song.file.name), 'song_id': str(new_song.id)}

    return HttpResponse(json.dumps(response_text), content_type="application/json")


@login_required
def treble(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    seg = song_to_audioseg(song)
    response_text = {'type': get_content_type(song.file.name), 'song_id': str(song.id)}

    if request.method == 'GET':
        return HttpResponse(json.dumps(response_text), content_type="application/json")

    form = AmplifyForm(request.POST)
    if not form.is_valid():
        return HttpResponse(json.dumps(response_text), content_type="application/json")

    start = float(form.cleaned_data['start']) * 1000
    end = float(form.cleaned_data['end']) * 1000
    amp = int(form.cleaned_data['amplify'])

    lower_seg = seg[:start]
    upper_seg = seg[end:]
    middle_seg = seg[start:end]

    middle_bass = middle_seg.low_pass_filter(20000)
    middle_bass = middle_bass.high_pass_filter(5200)
    middle_bass = middle_bass.apply_gain(amp-1)

    middle_seg = middle_seg.overlay(middle_bass)

    seg = lower_seg + middle_seg + upper_seg

    #export new song
    new_song = export_edit(seg, song)

    response_text = {'type': get_content_type(new_song.file.name), 'song_id': str(new_song.id)}

    return HttpResponse(json.dumps(response_text), content_type="application/json")


@login_required
def reverse(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    seg = song_to_audioseg(song)
    response_text = {'type': get_content_type(song.file.name), 'song_id': str(song.id)}

    if request.method == 'GET':
        return HttpResponse(json.dumps(response_text), content_type="application/json")

    form = ReverseForm(request.POST)

    if not form.is_valid():
        return HttpResponse(json.dumps(response_text), content_type="application/json")

    start = float(form.cleaned_data['start']) * 1000
    end = float(form.cleaned_data['end']) * 1000

    lower_seg = seg[:start]
    upper_seg = seg[end:]
    middle_seg = seg[start:end]

    new_seg = lower_seg + middle_seg.reverse() + upper_seg
    new_song = export_edit(new_seg, song)
    response_text = {'type': get_content_type(new_song.file.name), 'song_id': str(new_song.id)}

    return HttpResponse(json.dumps(response_text), content_type="application/json")


@login_required
def slice(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    seg = song_to_audioseg(song)
    response_text = {'type': get_content_type(song.file.name), 'song_id': str(song.id)}

    if request.method == 'GET':
        return HttpResponse(json.dumps(response_text), content_type="application/json")

    form = ReverseForm(request.POST)

    if not form.is_valid():
        return HttpResponse(json.dumps(response_text), content_type="application/json")

    start = float(form.cleaned_data['start']) * 1000
    end = float(form.cleaned_data['end']) * 1000

    lower_seg = seg[:start]
    upper_seg = seg[end:]

    new_seg = lower_seg + upper_seg
    if len(new_seg) <= 0:
        return HttpResponse(json.dumps(response_text), content_type="application/json")

    new_song = export_edit(new_seg, song)
    response_text = {'type': get_content_type(new_song.file.name), 'song_id': str(new_song.id)}

    return HttpResponse(json.dumps(response_text), content_type="application/json")


@login_required
def amplify(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    seg = song_to_audioseg(song)
    response_text = {'type': get_content_type(song.file.name), 'song_id': str(song.id)}

    if request.method == 'GET':
        return HttpResponse(json.dumps(response_text), content_type="application/json")

    form = AmplifyForm(request.POST)

    if not form.is_valid():
        return HttpResponse(json.dumps(response_text), content_type="application/json")

    amp = int(form.cleaned_data['amplify'])
    start = float(form.cleaned_data['start'])*1000
    end = float(form.cleaned_data['end'])*1000

    lower_seg = seg[:start]
    upper_seg = seg[end:]
    middle_seg = seg[start:end]
    middle_seg = middle_seg.apply_gain(amp)
    new_seg = lower_seg + middle_seg + upper_seg
    new_song = export_edit(new_seg, song)

    response_text = {'type': get_content_type(new_song.file.name), 'song_id': str(new_song.id)}

    return HttpResponse(json.dumps(response_text), content_type="application/json")


########################
### Helper Functions ###
########################
@login_required
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
    new_edit_number = old_song.edit_number + 1
    ext = get_ext(old_song.file.name)
    root = get_root(old_song.file.path)
    if old_song.edit_number > 0:
        root = root.replace("-" + str(old_song.edit_number), "")
    new_file_path = root + "-" + str(new_edit_number) + ext

    #export song to new file
    f = audio_seg.export(new_file_path, format=ext[1:])
    f.close()

    new_song = Song(name=old_song.name, file=new_file_path, edit_number=new_edit_number, project=old_song.project)
    new_song.save()

    return new_song


def get_content_type(filename):
    return guess_type(filename)[0]


def get_ext(filename):
    return os.path.splitext(filename)[1]


def get_root(filename):
    return os.path.splitext(filename)[0]