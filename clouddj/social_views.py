# Social actions for clouddj

from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from clouddj.models import *
from clouddj.forms import *
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.db import transaction
from datetime import datetime
from django.http import HttpResponse, Http404
from mimetypes import guess_type
from django.contrib.auth import update_session_auth_hash
import json
from clouddj.music_views import get_root, get_content_type, delete
import datetime
import math
from pydub import AudioSegment

def home(request):
    profiles = Profile.objects.all()
    context = {}
    context['search_form'] = SearchForm()
    context['user'] = request.user
    context['profiles'] = profiles
    return render(request, 'home.html', context)


@login_required
def add_post(request, id):
    form = PostForm(request.POST, request.FILES)
    if not form.is_valid():
        print form.errors
        return redirect(request.META['HTTP_REFERER'])

    song = get_object_or_404(Song, id=id)

    song.project.status = "complete"
    song.project.save()

    new_post = form.save()
    new_post.profile = request.user.profile
    new_post.song = song
    new_post.save()
    new_post.setHashtags()
    # if it's a competition post, add it to competition submissions
    competition = song.project.competition
    if competition:
        # check if it's still in time range
        time = datetime.datetime
        if competition.start <= time and time <= competition.end and \
           (request.user.profile not in competition.participants.all()):
            competition.submissions.add(new_post)
            competition.participants.add(request.user.profile)

    return redirect("/clouddj/stream")



@login_required
def rate(request,id):
    print "rating"

    post = get_object_or_404(Post, id = id)
    print post.id
    data = {}
    data['post_id'] = id
    rating=request.POST['rateval']

    # get the competition for the post if it exists
    try:
        competition = post.comp.all()[:1].get()
        time = datetime.datetime
        # if the user (isn't judge or creator) or (competition is over)
        # don't let them rate it!
        if ((request.user.profile not in competition.judges.all()) and \
            request.user.profile != competition.creator) or \
            time >= competition.end:
            return redirect(request.META.get('HTTP_REFERER'))
    except ObjectDoesNotExist:
        pass

    try: 
        userrating = Rating.objects.get(profile = request.user.profile, post = post)
        print "i already rated"

        numratings=int(post.numratings)
        olduserrating = userrating.rating
        overallrating = float(post.overallrating)

        new_ratings = (numratings * overallrating) 
        new_ratingsa = new_ratings + int(rating) - int(olduserrating)
        new_rating = new_ratingsa/numratings

        post.overallrating = new_rating
        post.showrating = int(post.overallrating)
        post.save()

        userrating.rating = rating
        userrating.save()

 
    except ObjectDoesNotExist:
        print "newrating"

        newrating = Rating(profile=request.user.profile, rating=rating, post=post)
        newrating.save()

        numratings=int(post.numratings)
        if (post.overallrating == None):
            overallrating = 0.0
        else:
            overallrating = float(post.overallrating)
        new_ratings = (numratings * overallrating) 
        new_ratingsa = new_ratings+ int(rating)
        new_num_ratings = numratings + 1
        new_rating = new_ratingsa/new_num_ratings
        post.overallrating = new_rating
        post.numratings = new_num_ratings
        post.showrating = int(post.overallrating)
        post.save()

    data['rating'] = rating
    return redirect(request.META.get('HTTP_REFERER'))
    

@login_required
def delete_post(request, id):

    post_to_delete = get_object_or_404(Post, profile=request.user.profile, id=id)
    delete(request, post_to_delete.song.id)
    post_to_delete.delete()

    data = {"post_id": id}

    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
def get_post_photo(request, id):

    post = get_object_or_404(Post, id=id)
    if not post.photo:
        raise Http404

    content_type = guess_type(post.photo.name)
    return HttpResponse(post.photo, content_type=content_type)


@login_required
def create_playlist(request):
    if request.method == 'GET':
        form = CreatePlaylistForm()
    else:
        form = CreatePlaylistForm(request.POST)
        if form.is_valid():
            new_playlist = Playlist(profile=get_object_or_404(Profile, user=request.user),
                                    name=form.cleaned_data['name'])
            new_playlist.save()

    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def add_to_playlist(request):
    if request.method == 'GET':
        form = PlaylistForm()
    else:
        form = PlaylistForm(request.POST)
        
        if not form.is_valid():
            return redirect(request.META.get('HTTP_REFERER'))
        
        playlist = Playlist.objects.get(id=form.cleaned_data['playlist'])

        if playlist.profile != request.user.profile:
            return redirect(request.META.get('HTTP_REFERER'))

        post = Post.objects.get(id=form.cleaned_data['post'])

        if post not in playlist.posts:
            playlist.posts.add(post)
            # no need to save() after this I think

    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def delete_from_playlist(request):
    if request.method == 'GET':
        form = PlaylistForm()
    else:
        form = PlaylistForm(request.POST)
        
        if not form.is_valid():
            return redirect(request.META.get('HTTP_REFERER'))
        
        playlist = Playlist.objects.get(id=form.cleaned_data['playlist'])

        if playlist.profile != request.user.profile:
            return redirect(request.META.get('HTTP_REFERER'))

        post = Post.objects.get(id=form.cleaned_data['post'])

        if post in playlist.posts:
            playlist.posts.remove(post)
            # no need to save() after this I think

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def playlists(request):
    context = {}
    context['profile'] = request.user.profile
    context['playlists'] = Playlist.objects.filter(profile=request.user.profile)
    context['search_form'] = SearchForm()
    context['playlist_form'] = PlaylistForm()

    return render(request, 'playlists.html', context)


@login_required
def stream(request):
    context = {}
    context['search_form'] = SearchForm()
    context['user'] = request.user
    context['profile'] = request.user.profile
    context['posts'] = Post.get_stream_posts(request.user.profile)
    context['playlists'] = Playlist.objects.filter(profile=request.user.profile)
    context['suggested_friends'] = suggested_friends(request.user.profile)

    profile = get_object_or_404(Profile, user=request.user)
    projects = Project.objects.filter(profile=profile, status="in_progress").order_by("-id")

    if projects:
        proj = projects[0]
        song = get_object_or_404(Song, edit_number=0, project=proj)
        name = get_root(song.file.name).replace("music/", "")
        song.name = name
        context['type'] = get_content_type(song.file.name)
        context['projects'] = projects

    return render(request, 'stream.html', context)


def suggested_friends(profile):
    suggested_friends = []
    for following in profile.following.all():
        for other_following in following.following.all():
            if other_following not in profile.following.all() and other_following != profile:
                suggested_friends.append(other_following)
    return suggested_friends

@login_required
def explore(request):
    context = {}
    context['search_form'] = SearchForm()
    context['user'] = request.user
    context['profile'] = request.user.profile
    context['suggested_posts'] = recommended_songs(request.user.profile)

    return render(request, 'explore.html', context)


@transaction.atomic
def register(request):
    context = {}

    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'signup.html', context)

    form = RegistrationForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'signup.html', context)

    # Creates the new user from the valid form data
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password1'],
                                        email=form.cleaned_data['email'])
    new_user.save()
    profile = Profile(user=new_user)
    profile.save()

    token = default_token_generator.make_token(new_user)
    email_body = """
        Welcome to cloudDJ. Please click the link below to verify your email address
        and complete the registration of your account:

        http://%s%s
    """ % (request.get_host(), reverse('confirm', args=(new_user.username, token)))

    send_mail(subject="Verify your email address",
              message=email_body,
              from_email="admin@clouddj.com",
              recipient_list=[new_user.email])

    context['email'] = form.cleaned_data['email']

    return render(request, 'needs-confirmation.html', context)

@transaction.atomic
def confirm_registration(request, username, token):
    user = get_object_or_404(User, username=username)

    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404

    # Otherwise token was valid, activate the user
    user.is_active = True
    user.save()
    return render(request, 'confirmation.html', {})




@login_required
def search(request):
    context = {}

    form = SearchForm(request.GET)
    context['search'] = form
    context['profile'] = request.user.profile
    context['user'] = request.user
    if not form.is_valid():
        return render(request, 'search.html', context)

    posts = Post.get_posts_containing(request.user.profile, form.cleaned_data['text'])
    profiles = Profile.get_user_named(form.cleaned_data['text'])

    context['message'] = str(int(len(posts))) + " result(s) found"

    context['posts'] = posts
    context['profiles'] = profiles

    return render(request, 'search.html', context)


@login_required
def add_comment(request, id):

    if not request.POST.get('comm', False):
        return

    post = get_object_or_404(Post, id=id)

    new_comment = Comment(profile=request.user.profile, post=post, text=request.POST['comm'])
    new_comment.save()

    data = {"comment": new_comment.text, "username": new_comment.profile.user.username, "post_id": id,
            "user_id": str(new_comment.profile.user.id)}

    return HttpResponse(json.dumps(data), content_type="application/json")




@login_required
def like(request, id):

    post = get_object_or_404(Post, id=id)
    data = {}
    data['post_id'] = id
    data['liked'] = "False"
    data['unliked'] = "False"

    if request.user.profile in post.likes.all():
        post.likes.remove(request.user.profile)
        post.save()
        data["unliked"] = "True"
        return HttpResponse(json.dumps(data), content_type="application/json")

    data["liked"] = "True"
    post.likes.add(request.user.profile)
    post.save()
    return HttpResponse(json.dumps(data), content_type="application/json")






@login_required
@transaction.atomic
def edit_profile(request):
    context = {}
    errors = []
    context['errors'] = errors
    context['profile'] = request.user.profile

    if request.method == 'GET':
        context['form'] = EditForm()
        return render(request, 'editprofile.html', context)

    form = EditForm(request.POST, request.FILES)
    context['form'] = form

    if not form.is_valid():
        print form.errors
        return render(request, 'editprofile.html', context)
    

    if form.cleaned_data['password1'] != "": 
        if request.user.check_password(form.cleaned_data['passwordc']):
            request.user.set_password(form.cleaned_data['password1'])
        else:
            errors.append("Current password is wrong.")
            context['errors'] = errors
            return render(request, 'editprofile.html', context)

    if form.cleaned_data['new_username'] != "":
        request.user.username = form.cleaned_data['new_username']
    if form.cleaned_data['new_email'] != "":
        request.user.email = form.cleaned_data['new_email']

    if request.FILES.get('photo', False):
        request.user.profile.photo = request.FILES.get('photo', False)

    request.user.profile.save()
    request.user.save()
    update_session_auth_hash(request, request.user)

    return render(request, 'editprofile.html', context)

@login_required
def profile(request, id):
    context = {}

    user_to_view = get_object_or_404(Profile, id=id)

    context['search'] = SearchForm()
    context['profile'] = user_to_view

    context['user'] = request.user
    context['posts'] = Post.get_user_posts(user_to_view)

    return render(request, 'profile.html', context)

@login_required
@transaction.atomic
def follow(request, id):
    user = get_object_or_404(Profile, id=id)
    logged_in = request.user.profile

    if logged_in in user.followers.all():
        user.followers.remove(logged_in)
    else:    
        user.followers.add(logged_in)

    user.save()
    return redirect(request.META.get('HTTP_REFERER'))


# returns list of recommended songs
@login_required
def recommended_songs(profile):
    num_songs = 5
    posts = profile.posts
    ratings = Rating.objects.filter(profile=profile)

    #genres = {}
    hts = {}
    for r in ratings.all():
        p = r.post
        mod_rating = (p.overallrating**2) * p.numratings

        for hashtag in p.hashtags.all():
            if hashtag in hts:
                hts[hashtag] = hts[hashtag] + mod_rating
            else:
                hts[hashtag] = mod_rating

    best_ht = None
    best_rating = 0

    for hashtag in hts:
        if hts[hashtag] > best_rating:
            best_rating = hts[hashtag]
            best_ht = hashtag

    if best_ht:
        return list(Post.objects.filter(hashtags=best_ht).order_by('-overallrating')[:num_songs])
    else:
        return list(Post.objects.order_by('-overallrating')[:num_songs])

#########################
### Competition stuff ###
#########################

@login_required
def create_competition(request):
    context = {}
    context['form'] = CompetitionForm()
    context['judgeform'] = JudgesForm()

    if request.method == 'GET':
        return render(request, 'create_competition.html', context)

    competition = Competition(creator=request.user.profile)
    form = CompetitionForm(request.POST, request.FILES, instance=competition)
    judgeform = JudgesForm(request.POST)

    if not form.is_valid() or not judgeform.is_valid():
        context['form'] = form
        context['judgeform'] = judgeform
        print form.errors
        return render(request, 'create_competition.html', context)

    competition = form.save()

    judges = judgeform.cleaned_data['judges'].split(' ')
    for judge in judges:
        if User.objects.filter(username=judge):
            j = User.objects.get(username=judge)
            competition.judges.add(Profile.objects.get(user=j))

    # redirect to competition page
    return redirect(reverse('competition', kwargs={'id':competition.id}))

@login_required
def edit_competition(request, id):
    # Can only edit BEFORE the competition starts
    context = {}
    context['form'] = EditCompetitionForm()
    context['judgeform'] = JudgesForm()
    context['removejudgeform'] = RemoveJudgesForm()

    if request.method == 'GET':
        return render(request, 'editcompetition.html', context)

    competition = get_object_or_404(Competition, id=id)
    if request.user.profile != competition.creator or \
       competition.start >= datetime.time:
        return redirect(request.META.get('HTTP_REFERER'))

    form = EditCompetitionForm(request.POST, request.FILES)
    judgeform = JudgesForm(request.POST)
    removejudgeform = RemoveJudgesForm(request.POST)

    if not (form.is_valid() and addform.is_valid() and removeform.is_valid()):
        return render(request, 'editcompetition.html', context)

    # don't save the new form instance

    if form.cleaned_data['base_sound']:
        competition.base_sound = form.cleaned_data['base_sound']
    if form.cleaned_data['start'] and form.cleaned_data['end']:
        competition.start = form.cleaned_data['start']
        competition.end = form.cleaned_data['end']
    if form.cleaned_data['description']:
        competition.description = form.cleaned_data['description']

    aj = judgeform.cleaned_data['judges'].split(' ')
    for judge in aj:
        if User.objects.filter(username=judge):
            j = User.objects.get(username=judge)
            competition.judges.add(Profile.objects.get(user=j))

    rj = removejudgeform.cleaned_data['rjudges'].split(' ')
    for judge in rj:
        if User.objects.filter(username=judge):
            j = User.objects.get(username=judge)
            competition.judges.remove(Profile.objects.get(user=j))

    competition.save()

    return redirect(reverse('competition', kwargs={'id':competition.id}))

# just add to regular rate...
@login_required
def rate_competition_submission(request, id):
    pass

# display competition page -> submissions
@login_required
def competition(request, id):
    # show creator, judges, description, then submissions
    # don't accept submissions, or release base music until comp starts
    # if competition is done, show like the winners and stuff
    context = {}
    competition = get_object_or_404(Competition, id=id)

    context['competition'] = competition
    context['posts'] = competition.submissions.all()
    # WRITE COMPETITION.HTML
    return render(request, 'competition.html', context)

## We could just put it under 'explore'
# shows all competitions
@login_required
def list_competitions(request):
    # don't care if it's get or post
    context = {}
    context['competitions'] = Competition.objects.all()

    # WRITE LISTCOMPETITIONS.HTML or add this to 'explore'
    return render(request, 'listcompetitions.html', context)        

# adds base sound for competition to the user's studio
@login_required
def join_competition(request, id):
    #if request.method == 'GET':
    #    return redirect(request.META.get('HTTP_REFERER'))

    profile = get_object_or_404(Profile, user=request.user)
    competition = get_object_or_404(Competition, id=id)

    time = datetime.datetime
    if (time < competition.start) or (profile in competition.participants.all()):
        return redirect(request.META.get('HTTP_REFERER'))

    new_project = Project(profile=profile, status="in_progress", competition=competition)
    new_project.save()

    # create copy of base music file
    ext = get_ext(competition.base_sound.name)
    root = get_root(competition.base_sound.path)

    audio_seg = AudioSegment.from_file(competition.base_sound.path, format=ext[1:])
    new_path = root + "_" + request.user.username + ext
    f = audio_seg.export(new_path)
    f.close()

    song = Song(name=competition.title, file=new_path, project=new_project)
    song.save()

    return redirect(reverse('studio'))


# change 'add_post'
# Now it posts your stuff, and also adds it to competition submissions

########################
### helper functions ###
########################

def get_ext(filename):
    L = filename.split('.')
    if len(L) == 0:
        return ''

    return '.'+L[-1]

def get_root(filename):
    L = filename.split('.')
    if len(L) == 0:
        return ''

    return '.'.join(L[:len(L)-1])


@login_required
def get_photo(request, id):

    profile = get_object_or_404(Profile, id=id)
    if not profile.photo:
        raise Http404

    content_type = guess_type(profile.photo.name)
    return HttpResponse(profile.photo, content_type=content_type)
