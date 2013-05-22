from django import forms
from django.forms.fields import ChoiceField
from django.forms.widgets import RadioSelect
from django.db import models
from models import *

class ClientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        try:
            self.initial['email'] = self.instance.user.email
            self.initial['first_name'] = self.instance.user.first_name
            self.initial['last_name'] = self.instance.user.last_name
        except User.DoesNotExist:
            pass
    email = forms.EmailField(label='Primary email', help_text='We will only use this email to notify you of our new stories.')
    first_name = forms.CharField(label='editor first name')
    last_name = forms.CharField(label='editor last name')
    class Meta:
        model = UserProfile
        password = forms.CharField(label='Password', help_text='')
        about = forms.CharField(label='Special Topics', help_text='Any special topics of interest to your audience?')
        pub_type = forms.ChoiceField(widget=forms.RadioSelect, choices=PUB_TYPES)
        fields = ['pub_name',
                  'pub_type',
                  'first_name',
                  'last_name',
                  'email',
                  'address',
                  'city',
                  'state',
                  'zipcode',
                  'pub_area',
                  'about',
                  'twitter',
                  'facebook',
                  'website']
        exclude = ['user', 
                   'user_type',
                   'can_publish',
                   'bio',
                   'byline',
                   'last_login',
                   'date_joined',
                   'is_staff',
                   'is_active',
                   'is_superuser',
                   'groups',
                   'user_permissions']
        
        
    def save(self, *args, **kwargs):
        """
        Update the primary email address, first & last name on the related User object as well.
        """
        u = self.instance.user
        u.email = self.cleaned_data['email']
        u.first_name = self.cleaned_data['first_name']
        u.last_name = self.cleaned_data['last_name']
        u.save()
        client = super(ClientForm, self).save(*args,**kwargs)
        return client

        """
        username = forms.EmailField(label='Email address', max_length=75)
        def clean_email(self):
            email = self.cleaned_data['username']
            return email
        
        
        """
