from django import forms
from django.forms import Form

from blog_app.models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)  # <input type='text'>
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)  # use <textarea>


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']


class SearchForm(forms.Form):
    query = forms.CharField()
