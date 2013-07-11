from django import forms
from django.forms.fields import ChoiceField
from django.forms.widgets import RadioSelect
from django.db import models
from models import *
from registration_email.forms import EmailRegistrationForm

class ClientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        try:
            self.initial['email'] = self.instance.user.email
            self.initial['first_name'] = self.instance.user.first_name
            self.initial['last_name'] = self.instance.user.last_name
        except User.DoesNotExist:
            pass
    email = forms.EmailField(label='Primary Email',
                             help_text='Where we will send new stories')
    first_name = forms.CharField(label='Editor first name')
    last_name = forms.CharField(label='Editor last name')
    pub_name = forms.CharField(label='News organization name')
    pub_type = forms.ChoiceField(choices=PUB_TYPES, label='News media type')
    #unsubscribe = forms.BooleanField(label='Unsubscribe from NNS Emails')
    
    class Meta:
        model = UserProfile
        password = forms.CharField(label='Password', help_text='')
        about = forms.CharField(label='Special Topics',
                                help_text='Any special topics of interest to your audience?')
        fields = ['pub_name','pub_type','first_name','last_name','email',
                  'phone','address','city','state','zipcode','pub_area',
                  'about','twitter','facebook','website']
        exclude = ['user','user_type','can_publish','bio','byline',
                   'last_login','date_joined','is_staff','is_active',
                   'is_superuser','groups','user_permissions'] 
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



class ReporterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReporterForm, self).__init__(*args, **kwargs)
        try:
            self.initial['email'] = self.instance.user.email
            self.initial['first_name'] = self.instance.user.first_name
            self.initial['last_name'] = self.instance.user.last_name
        except User.DoesNotExist:
            pass
    email = forms.EmailField(label='Primary email',
                             help_text='Your NNS Email Account')
    first_name = forms.CharField(label='First name')
    last_name = forms.CharField(label='Last name')
    class Meta:
        model = UserProfile
        password = forms.CharField(label='Password', help_text='')
        bio = forms.CharField(label='Reporter beats',
                                help_text='What will you focus on in your reporting?')
        fields = ['first_name','last_name','email','phone','bio','byline']
        exclude = ['pub_name','pub_type','user','user_type','can_publish','about',
                   'last_login','date_joined','is_staff','is_active',
                   'address','city','state','zipcode','pub_area','twitter','facebook','website',
                   'is_superuser','groups','user_permissions'] 
    def save(self, *args, **kwargs):
        """
        Update the primary email address, first & last name on the related User object as well.
        """
        u = self.instance.user
        u.email = self.cleaned_data['email']
        u.first_name = self.cleaned_data['first_name']
        u.last_name = self.cleaned_data['last_name']
        u.save()
        reporter = super(ReporterForm, self).save(*args,**kwargs)
        return reporter

def check_unsubscribe(unsubscribe):
        if unsubscribe:
            return 'InactiveClient'
        else:
            return 'Client'
        
class UnsubscribeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UnsubscribeForm, self).__init__(*args, **kwargs)
        try:
            self.initial['email'] = self.instance.user.email
            self.initial['first_name'] = self.instance.user.first_name
            self.initial['last_name'] = self.instance.user.last_name
        except User.DoesNotExist:
            pass
    email = forms.EmailField(label='Primary Email')
    first_name = forms.CharField(label='Editor first name')
    last_name = forms.CharField(label='Editor last name')    
    unsubscribe = forms.BooleanField(label='Unsubscribe from NNS Emails')
    
    class Meta:
        model = UserProfile
        fields = ['first_name','last_name','email','unsubscribe']


    def save(self, *args, **kwargs):
        u = self.instance.user
        p = self.instance.user.get_profile()
        u.email = self.cleaned_data['email']
        u.first_name = self.cleaned_data['first_name']
        u.last_name = self.cleaned_data['last_name']
        if self.cleaned_data['unsubscribe']:
            p.user_type = 'InactiveClient'
        u.save()
        p.save()
        client = super(UnsubscribeForm, self).save(*args,**kwargs)
        return client
        
         
        
