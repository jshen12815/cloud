import os
from django import forms
from clouddj.models import *


class UploadMusicForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ('file',)
        exclude = ('edit_number', 'project', 'name')

    def clean_file(self):
        form_file = self.cleaned_data.get('file')
        #ext = get_ext(form_file.name)
        ext = os.path.splitext(form_file.name)[1]

        valid_extentions = ['.mp3', '.wav', '.ogg']
        if not ext in valid_extentions:
            raise forms.ValidationError("Invalid file type.")

        return form_file


class RecordForm(forms.Form):
    start_min = forms.IntegerField(initial=0)
    start_sec = forms.IntegerField(initial=0, max_value=59)

    def clean(self):
        cleaned_data = super(RecordForm, self).clean()
        start_min = cleaned_data.get('start_min')
        start_sec = cleaned_data.get('start_sec')

        if start_min < 0 or start_sec < 0:
            raise forms.ValidationError("Must use positive values.")


class FilterForm(forms.Form):
    high_cutoff = forms.IntegerField(required=False)
    low_cutoff = forms.IntegerField(required=False)

    def clean(self):
        cleaned_data = super(FilterForm, self).clean()
        high_cutoff = cleaned_data.get('high_cutoff')
        low_cutoff = cleaned_data.get('low_cutoff')

        if high_cutoff < 0 or low_cutoff < 0:
            raise forms.ValidationError("Must use positive values.")

        if not high_cutoff and not low_cutoff:
            raise forms.ValidationError("Please enter a value.")


class FadeInForm(forms.Form):
    seconds = forms.IntegerField()


class FadeOutForm(forms.Form):
    seconds = forms.IntegerField()


class RepeatForm(forms.Form):
    start = forms.IntegerField()
    end = forms.IntegerField()
    iters = forms.IntegerField()


class SpeedupForm(forms.Form):
    multiplier = forms.DecimalField(required=False, max_digits=5, decimal_places=3)

    def clean_multiplier(self):
        mult = self.cleaned_data.get('clean_multiplier')
        if mult <= 0.0:
            raise forms.ValidationError("Multiplier must be nonnegative")

        return mult


class ReverseForm(forms.Form):
    start = forms.IntegerField()
    end = forms.IntegerField()


class CreatePlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ('name',)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("Playlist name cannot be empty")

        return name

class PlaylistForm(forms.Form):
    post = forms.IntegerField()
    playlist = forms.IntegerField()

    def clean(self):
        cleaned_data = super(AddToPlaylistForm, self).clean()

        return cleaned_data

    def clean_post(self):
        post = self.cleaned_data.get('post')
        if not Post.objects.filter(id=post):
            raise forms.ValidationError("Invalid post")

        return post

    def clean_playlist(self):
        playlist = self.cleaned_data.get('playlist')
        if not Playlist.objects.filter(id=playlist):
            raise forms.ValidationError("Invalid playlist")

        return playlist

class SliceForm(forms.Form):
    start = forms.IntegerField()
    end = forms.IntegerField()


class AmplifyForm(forms.Form):
    amplify = forms.IntegerField()
    beginning = forms.IntegerField()
    end = forms.IntegerField()


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=200)
    password1 = forms.CharField(max_length=200,
                                label='Password',
                                widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=200,
                                label='Confirm password',
                                widget=forms.PasswordInput())
    email = forms.EmailField(max_length=200)

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username already in use.")

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__exact=email):
            raise forms.ValidationError("Account with this email address already exists.")

        return email


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('profile', 'plays', 'date', )
        widgets = {
            'picture': forms.FileInput()
        }


class SearchForm(forms.Form):
    text = forms.CharField(max_length=200)