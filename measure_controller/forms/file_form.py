from django import forms

class FileForm(forms.Form):
    file_name = forms.CharField(label='file', max_length=100, widget=forms.TextInput(attrs={'class' : 'file'}))