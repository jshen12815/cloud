import os
from django import forms
from clouddj.models import *


class UploadMusicForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ('file',)
        exclude = ('edit_number', 'project',)

    def clean_file(self):
        form_file = self.cleaned_data.get('file')
        #ext = get_ext(form_file.name)
        ext = os.path.splitext(form_file.name)[1]

        valid_extentions = ['.mp3', '.wav', '.ogg']
        if not ext in valid_extentions:
            raise forms.ValidationError("Invalid file type.")

        return form_file


class RecordForm(forms.Form):
    start_min = models.IntegerField(default=0)
    start_sec = models.IntegerField(default=0)


class FilterForm(forms.Form):
    high_cutoff = models.IntegerField()
    low_cutoff = models.IntegerField()


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
