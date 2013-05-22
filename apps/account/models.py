from django.db import models
import datetime
from django.utils import timezone
from django import forms
from django.contrib.localflavor.us.models import USStateField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from registration.signals import *

USER_TYPES = (
    ('Editor', 'Editor'),
    ('Reporter', 'Reporter'),
    ('Client', 'Client'),
)

PUB_TYPES = (
    ('Newspaper', 'Newspaper'),
    ('Radio', 'Radio'),
    ('Television', 'Television'),
    ('Online', 'Online'),
    ('Other', 'Other'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='Client')
    about = models.TextField(blank=True, null=True, verbose_name="Special Topics")
    can_publish = models.BooleanField(default=False)
    bio = models.CharField(max_length=2000, blank=True, null=True)
    byline = models.CharField(max_length=75, blank=True, null=True)
    """ Client Profile Fields """
    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = USStateField(blank=True, null=True, default="NE")
    zipcode = models.CharField(max_length=5, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    pub_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Publication Name")
    pub_type = models.CharField(max_length=10, choices=PUB_TYPES, blank=True, null=True)
    pub_area = models.CharField(max_length=100, blank=True, null=True, verbose_name="Circulation Area")
    twitter = models.CharField(max_length=150, blank=True, null=True)
    facebook = models.CharField(max_length=150, blank=True, null=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    # notes       = models.ForeignKey(Notes)
    def get_absolute_url(self):
        return ('profiles_profile_detail', (), { 'username': self.user.username })
    def __unicode__(self):
        return self.user.username
    
    get_absolute_url = models.permalink(get_absolute_url)

def create_profile(sender, **kwargs):
    user = kwargs['instance']
    if kwargs['created']:
        up = UserProfile(user=user)
        up.save()  

post_save.connect(create_profile, sender=User)
