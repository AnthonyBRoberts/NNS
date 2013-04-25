from django.db import models
import datetime
from django.utils import timezone
from django import forms
from django.contrib.localflavor.us.models import USStateField
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __unicode__(self):
        return self.question
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField()
    def __unicode__(self):
        return self.choice

    
USER_TYPES = (
    ('Editor', 'Editor'),
    ('Reporter', 'Reporter'),
    ('Client', 'Client'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, unique=True)
    about = models.TextField(blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='Client')

    def save(self, *args, **kwargs):
        try:
           existing = Profile.objects.get(user=self.user)
           self.id = existing.id  #force update instead of insert 
        except Profile.DoesNotExist:
           print "Profile not created yet"
        models.Model.save(self, *args, **kwargs) 

def create_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user, sender=Profile)

class Editor(User):
    """ Editor User Profile """
    # user        = models.OneToOneField(User, related_name='editor', unique=True)
    can_publish = models.BooleanField(default=True)
    bio         = models.CharField(max_length=2000)
    # notes       = models.ForeignKey(Notes)
    def __unicode__(self):
        return self.last_name

class Reporter(User):
    """ Reporter User Profile """
    # user        = models.OneToOneField(User, related_name='reporter', unique=True)
    bio         = models.CharField(max_length=2000)
    byline      = models.CharField(max_length=75)
    # notes       = models.ForeignKey(Notes)
    def __unicode__(self):
        return self.last_name

class Client(User):
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
        return self.last_name
