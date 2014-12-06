import os
from django import forms
from clouddj.models import *
from django.forms.widgets import RadioSelect
from datetimewidget.widgets import DateTimeWidget

class UploadMusicForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ('file','name')
        exclude = ('edit_number', 'project',)

    def clean_file(self):
        form_file = self.cleaned_data.get('file')
        ext = os.path.splitext(form_file.name)[1]

        valid_extentions = ['.mp3', '.wav', '.ogg']
        if not ext in valid_extentions:
            raise forms.ValidationError("Invalid file type.")

        return form_file


class RecordForm(forms.Form):
    start = forms.FloatField(initial=0)

    def clean(self):
        cleaned_data = super(RecordForm, self).clean()
        start = cleaned_data.get('start')

        if start < 0:
            raise forms.ValidationError("Must use positive values.")

        return cleaned_data




class FilterForm(forms.Form):
    start = forms.FloatField(required=False)
    end = forms.FloatField(required=False)
    high_cutoff = forms.FloatField(required=False)
    low_cutoff = forms.FloatField(required=False)

    def clean(self):
        cleaned_data = super(FilterForm, self).clean()
        high_cutoff = cleaned_data.get('high_cutoff')
        low_cutoff = cleaned_data.get('low_cutoff')

        if not high_cutoff and not low_cutoff:
            raise forms.ValidationError("Please enter a value.")


class FadeInForm(forms.Form):
    start = forms.IntegerField()
    end = forms.IntegerField()


class FadeOutForm(forms.Form):
    start = forms.IntegerField()
    end = forms.IntegerField()


class RepeatForm(forms.Form):
    start = forms.FloatField()
    end = forms.FloatField()
    iters = forms.IntegerField()


class EchoForm(forms.Form):
    start = forms.FloatField()
    end = forms.FloatField()
    delay = forms.IntegerField()
    decay = forms.IntegerField()


class SpeedupForm(forms.Form):
    start = forms.FloatField()
    end = forms.FloatField()
    multiplier = forms.FloatField()

    def clean_multiplier(self):
        mult = self.cleaned_data.get('multiplier')
        if mult <= 1.0:
            raise forms.ValidationError("Multiplier must be positive")

        return mult


class ReverseForm(forms.Form):
    start = forms.FloatField()
    end = forms.FloatField()


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
    start = forms.FloatField()
    end = forms.FloatField()


class AmplifyForm(forms.Form):
    amplify = forms.IntegerField()
    start = forms.FloatField()
    end = forms.FloatField()


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
    photo = forms.FileField(required=False)

    class Meta:
        model = Post
        exclude = ('profile', 'plays', 'date', 'song', 'hashtags', 'numratings','overallratings', 'showrating' )
        widgets = {
            'photo': forms.FileInput()
        }


class SearchForm(forms.Form):
    text = forms.CharField(max_length=200)


class EditForm(forms.Form):
    new_username = forms.CharField(max_length =20,
                                label = 'New Username',
                                widget = forms.TextInput(attrs = {"class": "form-control"}),
                                required = False)
    new_email = forms.CharField(max_length = 20,
                                widget = forms.TextInput(attrs = {"class": "form-control", "input type": "email"}),
                                label = 'New Email',
                                required = False)
    passwordc = forms.CharField(max_length = 200, 
                                label='Current Password', 
                                widget = forms.PasswordInput(attrs = {"class": "form-control"}),
                                required = False)
    password1 = forms.CharField(max_length = 200, 
                                label='New Password', 
                                widget = forms.PasswordInput(attrs = {"class": "form-control"}),
                                required = False)
    password2 = forms.CharField(max_length = 200, 
                                label='Re-enter password',  
                                widget = forms.PasswordInput(attrs = {"class": "form-control"}),
                                required = False)

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(EditForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # Generally return the cleaned data we got from our parent.
        return cleaned_data

    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        new_username = self.cleaned_data.get('new_username')
        if User.objects.filter(username__exact=new_username):
            raise forms.ValidationError("Username is already taken.")

        # Generally return the cleaned data we got from the cleaned_data
        # dictionary
        return new_username

class JudgesForm(forms.Form):
    judges = forms.CharField(max_length=4200, 
                            label = 'Judges',
                            widget = forms.TextInput(attrs={'class':'form-control', 'placeholder':'judges'}),
                            required=False)

class CompetitionForm(forms.ModelForm):

    class Meta:
        model = Competition
        fields = ('title', 'description', 'start', 'end', 'base_sound')
        #exclude = ('creator', 'participants', 'submissions', 'judges')

        dateTimeOptions = {
            'format': 'mm/dd/yyyy HH:ii'
        }

        widgets = {
            # 'judges': forms.TextInput(attrs={'class':'form-control'}),
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'title'}),
            'description': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'description'}),
            'start': DateTimeWidget(bootstrap_version=3, options=dateTimeOptions),
            'end': DateTimeWidget(bootstrap_version=3, options=dateTimeOptions)
        }

    def clean_end(self):
        start = self.cleaned_data['start']
        end = self.cleaned_data['end']

        if start > end:
            raise forms.ValidationError("Competition must end after it starts")

        return end

    def clean_base_sound(self):
        base_file = self.cleaned_data.get('base_sound')
        ext = os.path.splitext(base_file.name)[1]

        valid_extentions = ['.mp3', '.wav', '.ogg']
        if not ext in valid_extentions:
            raise forms.ValidationError("Invalid file type.")

        return base_file

class EditCompetitionForm(forms.ModelForm):
    addJudges = forms.TextInput(attrs={'class':'form-control'})
    removeJudges = forms.TextInput(attrs={'class':'form-control'})

    class Meta:
        model = Competition
        fields = ('description', 'start', 'end', 'base_sound')

    def clean_base_sound(self):
        base_file = self.cleaned_data.get('base_sound')
        if not base_file:
            return None

        ext = os.path.splitext(base_file.name)[1]

        valid_extentions = ['.mp3', '.wav', '.ogg']
        if not ext in valid_extentions:
            raise forms.ValidationError("Invalid file type.")

        return base_file

    def clean_end(self):
        start = self.cleaned_data['start']
        end = self.cleaned_data['end']

        if not start or not end:
            return None

        if start > end:
            raise forms.ValidationError("Competition must end after it starts")

        return end
