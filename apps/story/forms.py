from django import forms
from models import Article, Edit
from tinymce.widgets import TinyMCE

class ArticleForm(forms.ModelForm):
    text = forms.CharField(widget=TinyMCE())
    email_text = forms.CharField(widget=TinyMCE())
    class Meta:
        model = Article
        #fields = ['title', 'text', 'publish_date', 'is_published', 'docfile']
        exclude = ['author', 'slug']

class EditForm(forms.ModelForm):
    class Meta:
        model = Edit
        fields = ['summary']
