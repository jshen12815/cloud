import os

from django import forms

from clouddj.models import *


class UploadMusicForm(forms.ModelForm):
    class Meta:
        model = Song

    def clean_file(self):
        ext = os.path.splitext(self.file.name)
        valid_extentions = ['.mp3', '.wav', '.ogg']
        if not ext in valid_extentions:
            raise forms.ValidationError("Invalid file type.")
