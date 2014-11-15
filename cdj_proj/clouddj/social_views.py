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


def home(request):
    profiles = Profile.objects.all()
    return render(request, 'index.html', {'profiles': profiles, 'user': request.user})


@login_required
def add_post(request):

    new_post = Post(user=request.user.person, date=datetime.now())
    form = PostForm(request.POST, request.FILES, instance=new_post)
    if not form.is_valid():
        return redirect(request.META['HTTP_REFERER'])

    form.save()

    return redirect(request.META['HTTP_REFERER'])


@login_required
def delete_post(request, id):

    post_to_delete = get_object_or_404(Post, user=request.user.profile, id=id)
    post_to_delete.delete()
    return redirect(request.META['HTTP_REFERER'])


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
            return render(request, 'home.html', {'user': request.user})

    # THIS TOO
    return render(request, 'home.html', {'form': form, 'user': request.user})

@login_required
def stream(request):
    return render(request, 'home.html', {'user': request.user})

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
