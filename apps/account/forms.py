from django import forms
from django.db import models
from models import *


class ClientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        try:
            # self.fields['user_type'].initial = self.instacne.user.user_type
            self.fields['email'].initial = self.instance.user.email
            # self.fields['first_name'].initial = self.instance.user.first_name
            # self.fields['last_name'].initial = self.instance.user.last_name
        except User.DoesNotExist:
            pass
    class Meta:
        model = Client
        exclude = ['user',
                   'user_type',
                   'about',
                   'last_login',
                   'first_name',
                   'last_name',
                   'date_joined',
                   'is_staff',
                   'is_active',
                   'is_superuser',
                   'groups',
                   'user_permissions']
        # username = forms.EmailField(label='Email address', max_length=75)
        password = forms.CharField(label='Password', help_text='')
        #def clean_email(self):
            #email = self.cleaned_data['username']
            #return email
        
        def save(self, *args, **kwargs):
            """
            Update the primary email address on the related User object as well.
            """
            u = self.instance.user
            u.email = self.cleaned_data['email']
            u.user_type = self.instance.user.user_type
            u.save()
            profile = super(ProfileForm, self).save(*args,**kwargs)
            return profile

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
