from django import forms
from models import Editor, Reporter, Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ['last_login',
                   'date_joined',
                   'is_staff',
                   'is_active',
                   'is_superuser',
                   'groups.all',
                   'user_permissions.all']

class ReporterForm(forms.ModelForm):
    class Meta:
        model = Reporter

class EditorForm(forms.ModelForm):
    class Meta:
        model = Editor      
