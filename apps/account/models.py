from django.db import models
import datetime
from django.utils import timezone
from django import forms
from django.contrib.localflavor.us.models import USStateField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from registration.signals import *
#from signals import create_user_profile

   
USER_TYPES = (
    ('Editor', 'Editor'),
    ('Reporter', 'Reporter'),
    ('Client', 'Client'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    about = models.TextField(blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='Client')   
    
    def get_absolute_url(self):
        return ('profiles_profile_detail', (), { 'username': self.user.username })

    def __unicode__(self):
        return self.user.username
    
    get_absolute_url = models.permalink(get_absolute_url)
    
    @property 
    def is_client(self):
        try:
            self.client
            return True
        except client.DoesNotExist:
            return False
        
    @property 
    def is_reporter(self):
        try:
            self.reporter
            return True
        except reporter.DoesNotExist:
            return False

    @property 
    def is_editor(self):
        try:
            self.editor
            return True
        except editor.DoesNotExist:
            return False  
    #def save(self, *args, **kwargs):
        #try:
           #existing = UserProfile.objects.get(user=self.user)
           #self.id = existing.id  #force update instead of insert 
        #except UserProfile.DoesNotExist:
           #print "Profile not created yet"
        #models.Model.save(self, *args, **kwargs) 

class Editor(UserProfile):
    """ Editor User Profile """
    # user        = models.OneToOneField(User, related_name='editor', unique=True)
    can_publish = models.BooleanField(default=True)
    bio         = models.CharField(max_length=2000)
    # notes       = models.ForeignKey(Notes)
    def __unicode__(self):
        return self.last_name

class Reporter(UserProfile):
    """ Reporter User Profile """
    # user        = models.OneToOneField(User, related_name='reporter', unique=True)
    bio         = models.CharField(max_length=2000)
    byline      = models.CharField(max_length=75)
    # notes       = models.ForeignKey(Notes)
    def __unicode__(self):
        return self.last_name

class Client(UserProfile):
    """ Client User Profile """
    # user        = models.OneToOneField(User, related_name='client')
    address     = models.CharField(max_length=100)
    city        = models.CharField(max_length=100)
    state       = USStateField(default="NE")
    zipcode     = models.CharField(max_length=5, blank=True, null=True)
    phone       = models.CharField(max_length=10)
    pub_area    = models.CharField(max_length=100, blank=True, null=True, verbose_name="Circulation Area")
    twitter     = models.CharField(max_length=150, blank=True, null=True)
    facebook    = models.CharField(max_length=150, blank=True, null=True)
    website     = models.URLField(max_length=200, blank=True, null=True)
    # notes       = models.ForeignKey(Notes)
    def __unicode__(self):
        return self.user.last_name
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
       UserProfile.objects.create(user=instance)
       
    #request, instance = kwargs['request'], kwargs['user']
    
    try:
        user_type = request.POST['user_type'].lower()
        if user_type == "client":  #user .lower for case insensitive comparison 
            Client(user = instance).save()
        elif user_type == "reporter":
            Reporter(user = instance).save()
        elif user_type == "editor":
            Editor(user = instance).save()
        else:
            UserProfile(user = instance).save()  #Default create - might want to raise error instead 
    except KeyError:
        UserProfile(user = instance).save()  #Default create just a profile

user_registered.connect(create_user_profile, sender=User)
