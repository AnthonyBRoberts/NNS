from django import forms
from models import Article, Edit
from tinymce.widgets import TinyMCE

class ArticleForm(forms.ModelForm):
    text = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 20}))
    class Meta:
        model = Article
        exclude = ['author', 'slug']

class EditForm(forms.ModelForm):
    class Meta:
        model = Edit
        fields = ['summary']
