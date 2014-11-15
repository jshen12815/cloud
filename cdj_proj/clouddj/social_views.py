# Social actions for clouddj
import re
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from clouddj.models import *
from clouddj.forms import *
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.db import transaction


def home(request):
    profiles = Profile.objects.all()
    return render(request, 'index.html', {'profiles': profiles})


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

            # NEED TO UPDATE THIS LATER
            return render(request, 'home.html', {})

    # THIS TOO
    return render(request, 'home.html', {'form': form})


def stream(request):
    return render(request, 'home.html', {})

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

    return render(request, 'needs_confirmation.html', context)

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
def add_comment(request):
    errors = []
    context = {}
    # Creates a new comment if it is present as a parameter in the request
    if not 'comment' in request.POST or not request.POST['comment']:
        errors.append('You must enter an comment to add.')
        print("Error")
    if not 'postID' in request.POST or not request.POST['postID']:
        errors.append('id')
    else:
        post = Post.objects.get(id =request.POST['postID'])
        new_comment = Comment(text=request.POST['comment'], post = post, profile = request.user)
        new_comment.save()
    comments = Comment.objects.filter(user=request.user)
    context = {'comments' : comments, 'errors' : errors}
    return redirect(request.META.get('HTTP_REFERER'))




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