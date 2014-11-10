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