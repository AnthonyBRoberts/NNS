from django import forms
from models import Article, Edit
from tinymce.widgets import TinyMCE

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['author', 'slug']

class EditForm(forms.ModelForm):
    class Meta:
        model = Edit
        fields = ['summary']
