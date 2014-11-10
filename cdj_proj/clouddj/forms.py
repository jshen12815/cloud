from django import forms

from clouddj.models import *
from clouddj.music_views import get_ext


class UploadMusicForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ('file',)

    def clean_file(self):
        form_file = self.cleaned_data.get('file')
        ext = get_ext(form_file.name)
        valid_extentions = ['.mp3', '.wav', '.ogg']
        if not ext in valid_extentions:
            raise forms.ValidationError("Invalid file type.")

        return form_file


class FilterForm(forms.Form):
    high_cutoff = models.IntegerField(blank=True)
    low_cutoff = models.IntegerField(blank=True)


class FadeInForm(forms.Form):
    seconds = forms.IntegerField()


class FadeOutForm(forms.Form):
    seconds = forms.IntegerField()


class RepeatForm(forms.Form):
    start = forms.IntegerField()
    end = forms.IntegerField()
    iters = forms.IntegerField()


class SpeedupForm(forms.Form):
    multiplier = forms.DecimalField(blank=False, max_digits=5, decimal_places=3)

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


class RecordForm(forms.Form):
    secs = models.IntegerField()
    filename = models.CharField(max_length=255)