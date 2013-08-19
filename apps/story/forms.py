from django import forms
from models import Article, Edit
from django.contrib.admin import widgets
from datetimewidget.widgets import DateTimeWidget
from suit_redactor.widgets import RedactorWidget
from tinymce.widgets import TinyMCE

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['author', 'slug']
        dateTimeOptions = {
            'format': 'mm/dd/yyyy HH:ii P',
            'autoclose': 'true',
            'showMeridian': 'false',
        }
        widgets = {
            'email_text': RedactorWidget(editor_options={'lang': 'en'}),
            'text': RedactorWidget(editor_options={'lang': 'en'}),
        }

class Article_EForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['slug']
        dateTimeOptions = {
            'format': 'mm/dd/yyyy HH:ii P',
            'autoclose': 'true',
            'showMeridian': 'false',
        }
        widgets = {
            'publish_date': DateTimeWidget(options = dateTimeOptions),
            'email_text': RedactorWidget(editor_options={'lang': 'en'}),
            'text': RedactorWidget(editor_options={'lang': 'en'}),
        }

class Article_RForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['author', 'byline', 'slug', 'publish_date', 'email_text', 'is_published', 'send_now', 'docfile']
        dateTimeOptions = {
            'format': 'mm/dd/yyyy HH:ii P',
            'autoclose': 'true',
            'showMeridian': 'false',
        }
        widgets = {
            'text': RedactorWidget(editor_options={'lang': 'en'})
        }


class EditForm(forms.ModelForm):
    class Meta:
        model = Edit
        fields = ['summary']
