from django import forms
from models import Editor, Reporter, Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ['last_login',
                   'first_name',
                   'last_name',
                   'date_joined',
                   'is_staff',
                   'is_active',
                   'is_superuser',
                   'groups',
                   'user_permissions']

class ReporterForm(forms.ModelForm):
    class Meta:
        model = Reporter

class EditorForm(forms.ModelForm):
    class Meta:
        model = Editor      
