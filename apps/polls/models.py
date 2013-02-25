from django.db import models
import datetime
from django.utils import timezone
from django import forms
from django.contrib.localflavor.us.models import USStateField
from django.contrib.auth.models import User
from django.db.models.signals import post_save



class Editor(User):
    """ Editor User Profile """
    # user        = models.OneToOneField(User, related_name='editor', unique=True)
    can_publish = models.BooleanField(default=True)
    bio         = models.CharField(max_length=2000)
    # notes       = models.ForeignKey(Notes)

class Reporter(User):
    """ Reporter User Profile """
    # user        = models.OneToOneField(User, related_name='reporter', unique=True)
    bio         = models.CharField(max_length=2000)
    byline      = models.CharField(max_length=75)
    # notes       = models.ForeignKey(Notes)


class Client(User):
    """ Client User Profile """
    # user        = models.OneToOneField(User, related_name='client')
    address     = models.CharField(max_length = 100)
    city        = models.CharField(max_length=100)
    state       = USStateField()
    zipcode     = models.CharField(max_length=5)
    pub_area    = models.CharField(max_length=100)
    phone       = models.CharField(max_length=10)
    twitter     = models.CharField(max_length=150)
    facebook    = models.CharField(max_length=150)
    website     = models.URLField(max_length=200)
    # notes       = models.ForeignKey(Notes)

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
"""
def create_editor_profile(sender, instance, created, **kwargs):
    if created:
        Editor.objects.create(user=instance)

post_save.connect(create_editor_profile, sender=User)
"""
