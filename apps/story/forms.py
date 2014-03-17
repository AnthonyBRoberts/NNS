from django import forms
from django.core.validators import validate_email
from models import Article, MediaItem
from django.contrib.admin import widgets
from datetimewidget.widgets import DateTimeWidget
from suit_redactor.widgets import RedactorWidget

EMAIL_OPTIONS = (
    ('send all', 'Send to All Clients'),
    ('broadcast only', 'Send to Broadcast Only'),
    ('additional only', 'Send to Additional Recipients Only'),
)

class MultiEmailField(forms.Field):
    def to_python(self, value):
        "Normalize data to a list of strings."

        # Return an empty list if no input was given.
        if not value:
            return []
        return value.split(',')

    def validate(self, value):
        "Check if value consists only of valid emails."

        # Use the parent's handling of required fields, etc.
        super(MultiEmailField, self).validate(value)

        for email in value:
            validate_email(email.strip(' '))
            

class Article_EForm(forms.ModelForm):

    send_now = forms.ChoiceField(widget=forms.RadioSelect(), required=False)
    add_recipients = MultiEmailField(label='Additional Recipients, multiple emails must be separated by a comma.', required=False)

    class Meta:
        model = Article
        fields = ('title', 'text', 'email_text', 'author', 'byline',
                    'tags', 'docfile', 'mediaitems', 'publish_date', 'is_published', 
                    'send_now', 'add_recipients'
                    )
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

    def __init__(self, *args, **kwargs):
        super(Article_EForm, self).__init__(*args, **kwargs)
        email_options = EMAIL_OPTIONS
        self.fields['send_now'].choices = email_options

    def clean(self):
        cleaned_data = super(Article_EForm, self).clean()
        add_recipients = cleaned_data.get("add_recipients")

        if cleaned_data.get('send_now') == 'additional only':
            if add_recipients == []:
                raise forms.ValidationError("You selected Send to Additional Recipients Only, but didn't include any additional recipients")
        return cleaned_data


class Article_RForm(forms.ModelForm):

    ready_for_editor = forms.BooleanField(label='Ready for editor', required=False)

    class Meta:
        model = Article
        fields = ('title', 'text', 'tags', 'docfile', 'ready_for_editor')
        exclude = ['author', 'byline', 'slug', 'publish_date', 'email_text', 'is_published', 'send_now', 'media']
        dateTimeOptions = {
            'format': 'mm/dd/yyyy HH:ii P',
            'autoclose': 'true',
            'showMeridian': 'false',
        }
        widgets = {
            'text': RedactorWidget(editor_options={'lang': 'en'})
        }

class Media_EForm(forms.ModelForm):

    send_now = forms.ChoiceField(widget=forms.RadioSelect(), required=False)
    add_recipients = MultiEmailField(label='Additional Recipients, multiple emails must be separated by a comma.', required=False)

    class Meta:
        model = MediaItem
        fields = ('title', 'text', 'email_text', 'author', 'byline',
                    'tags', 'docfile', 'publish_date', 'is_published', 
                    'send_now', 'add_recipients'
                    )
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

    def __init__(self, *args, **kwargs):
        super(Media_EForm, self).__init__(*args, **kwargs)
        email_options = EMAIL_OPTIONS
        self.fields['send_now'].choices = email_options

    def clean(self):
        cleaned_data = super(Media_EForm, self).clean()
        add_recipients = cleaned_data.get("add_recipients")

        if cleaned_data.get('send_now') == 'additional only':
            if add_recipients == []:
                raise forms.ValidationError("You selected Send to Additional Recipients Only, but didn't include any additional recipients")
        return cleaned_data


class Media_RForm(forms.ModelForm):

    ready_for_editor = forms.BooleanField(label='Ready for editor', required=False)

    class Meta:
        model = MediaItem
        fields = ('title', 'text', 'tags', 'docfile', 'ready_for_editor')
        exclude = ['author', 'byline', 'slug', 'publish_date', 'email_text', 'send_now', 'is_published']
        dateTimeOptions = {
            'format': 'mm/dd/yyyy HH:ii P',
            'autoclose': 'true',
            'showMeridian': 'false',
        }
        widgets = {
            'text': RedactorWidget(editor_options={'lang': 'en'})
        }