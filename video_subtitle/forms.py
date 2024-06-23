from django import forms

class VideoUploadForm(forms.Form):
    video = forms.FileField()

class SearchForm(forms.Form):
    keyword = forms.CharField(max_length=100, required=False, label='Search')