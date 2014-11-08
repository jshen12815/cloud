import os

from django import forms

from clouddj.models import *


class UploadMusicForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ('file',)

    def clean_file(self):
        form_file = self.cleaned_data.get('file')
        ext = os.path.splitext(form_file.name)
        valid_extentions = ['.mp3', '.wav', '.ogg']
        if not ext in valid_extentions:
            raise forms.ValidationError("Invalid file type.")

        return form_file
