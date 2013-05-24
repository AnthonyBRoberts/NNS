from django import forms
from models import Article, Edit
from tinymce.widgets import TinyMCE

class ArticleForm(forms.ModelForm):
    text = forms.CharField(widget=TinyMCE(attrs={'cols': 20, 'rows': 20}))
    class Meta:
        model = Article
        fields = ['title', 'text', 'publish_date', 'is_published', 'docfile']
        exclude = ['author', 'slug']
        #widgets = {
        #    'text': TinyMCE(attrs={'cols': 80, 'rows': 20}),
        #}

class EditForm(forms.ModelForm):
    class Meta:
        model = Edit
        fields = ['summary']
