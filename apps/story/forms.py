from django import forms
from models import Article, Edit
from django.contrib.admin import widgets
from datetimewidget.widgets import DateTimeWidget
from tinymce.widgets import TinyMCE

class ArticleForm(forms.ModelForm):
    text = forms.CharField(widget=TinyMCE())
    email_text = forms.CharField(widget=TinyMCE())
    class Meta:
        model = Article
        exclude = ['author', 'slug']
        dateTimeOptions = {
            'format': 'mm/dd/yyyy HH:ii P',
            'autoclose': 'true',
            'showMeridian': 'false',
        }
        widgets = {
            'publish_date': DateTimeWidget(options = dateTimeOptions)
        }

class EditForm(forms.ModelForm):
    class Meta:
        model = Edit
        fields = ['summary']
