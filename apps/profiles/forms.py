from django import forms
from models import Editor, Reporter, Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ['email',
                   'last_login',
                   'first_name',
                   'last_name',
                   'date_joined',
                   'is_staff',
                   'is_active',
                   'is_superuser',
                   'groups',
                   'user_permissions']
        username = forms.EmailField(label='Email address',
                                    max_length=75)
        password = forms.CharField(label='Password', help_text='')
        def clean_email(self):
            email = self.cleaned_data['username']
            return email

class ReporterForm(forms.ModelForm):
    class Meta:
        model = Reporter
        exclude = ['last_login',
                   'date_joined',
                   'is_staff',
                   'is_active',
                   'is_superuser',
                   'groups',
                   'user_permissions']

class EditorForm(forms.ModelForm):
    class Meta:
        model = Editor      
