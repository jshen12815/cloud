# Social actions for clouddj

from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.core.urlresolvers import reverse
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
        return redirect(request.META['HTTP_REFERER'])

    song = get_object_or_404(Song, id=id)
    song.project.status = "complete"
    song.project.save()

    new_post = form.save()
    new_post.profile = request.user.profile
    new_post.song = song
    new_post.save()

    return redirect("/clouddj/stream")


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
def stream(request):
    context = {}
    context['search_form'] = SearchForm()
    context['user'] = request.user
    context['profile'] = request.user.profile
    context['posts'] = Post.get_stream_posts(request.user.profile)

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


@login_required
def explore(request):
    context = {}
    context['search_form'] = SearchForm()
    context['user'] = request.user
    context['profile'] = request.user.profile

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
    context['user'] = request.user
    if not form.is_valid():
        return render(request, 'search.html', context)

    posts = Post.get_posts_containing(request.user.profile, form.cleaned_data['text'])

    context['message'] = str(int(len(posts))) + " result(s) found"

    context['posts'] = posts

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
def rate(request,id):
    print "hi"
    if id:
        rating=Rating.objects.get(id=id)
        num_ratings = rating.numratings
        cur_rating = rating.rating
        my_rating = request.POST['rating']
        new_ratings = (num_ratings * cur_rating) + new_rating
        new_num_ratings = num_ratings + 1
        new_rating = new_ratings/new_num_ratings
        rating.rating = new_rating
        rating.numratings = new_num_ratings
        rating.save
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
@transaction.atomic
def edit_profile(request):
    context = {}
    errors = []
    context['errors'] = errors

    if request.method == 'GET':
        context['form'] = EditForm()
        return render(request, 'editprofile.html', context)

    form = EditForm(request.POST)
    context['form'] = form

    if not form.is_valid():
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

    request.user.save()
    update_session_auth_hash(request, request.user)

    return render(request, 'editprofile.html', context)

@login_required
def profile(request, id):
    context = {}

    user_to_view = get_object_or_404(Profile, id=id)

    context['search'] = SearchForm()
    context['prof_owner'] = user_to_view

    context['user'] = request.user

    return render(request, 'profile.html', context)

@login_required
@transaction.atomic
def follow(request, id):
    user = get_object_or_404(Profile, id=id)
    logged_in = request.user.profile
    data = {}
    data['followed'] = "False"
    data['unfollowed'] = "False"

    if logged_in in user.followers.all():
        user.followers.remove(logged_in)
        data['unfollowed'] = "True"
    else:    
        user.followers.add(logged_in)
        data['followed'] = "True"

    user.save()
    return HttpResponse(json.dumps(data), content_type="application/json")


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
        mod_rating = (r.rating**2) * r.numratings

        for hashtag in p.hashtags.all():
            if hashtag in hts:
                hts[hashtag] = hts[hashtag] + mod_rating
            else:
                hts[hashtag] = mod_rating

    best_ht = None
    best_rating = 0

    for hashtag in hts:
        if hts[hashtag] >= best_rating:
            best_rating = hts[hashtag]
            best_ht = hashtag

    print list(Post.objects.order_by('-plays')[:num_songs])
    return list(Post.objects.order_by('-plays')[:num_songs])

