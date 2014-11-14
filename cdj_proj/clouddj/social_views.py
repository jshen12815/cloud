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
    render(request, 'home.html', {'form': form})


def stream(request):
    return render(request, 'home.html', {})


def register(request):
    context = {}

    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        return render(request, 'signup.html', context)

    errors = []
    context['errors'] = errors

    # Checks the validity of the form data
    if not 'username' in request.POST or not request.POST['username']:
        errors.append('Username is required.')
    else:
        # Save the username in the request context to re-fill the username
        # field in case the form has errrors
        context['username'] = request.POST['username']

    if not 'password1' in request.POST or not request.POST['password1']:
        errors.append('Password is required.')
    if not 'password2' in request.POST or not request.POST['password2']:
        errors.append('Confirm password is required.')

    if 'password1' in request.POST and 'password2' in request.POST and request.POST['password1'] and request.POST[
            'password2'] and request.POST['password1'] != request.POST['password2']:
        errors.append('Passwords did not match.')

    if len(User.objects.filter(username=request.POST['username'])) > 0:
        errors.append('Username is already taken.')

    if errors:
        return render(request, 'signup.html', context)

    # Creates the new user from the valid form data
    new_user = User.objects.create_user(first_name=request.POST['first_name'],
                                        last_name=request.POST['last_name'],
                                        username=request.POST['username'],
                                        password=request.POST['password1'],
                                        email=request.POST['email'])
    new_user.save()

    # Logs in the new user and redirects to home
    new_user = authenticate(username=request.POST['username'],
                            password=request.POST['password1'])
    login(request, new_user)
    return redirect('/')