from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
from taggit.managers import TaggableManager
from tools.killgremlins import killgremlins
from notifications import notify
import datetime

class MediaItem(models.Model):
	"""Represents a story article"""
	
	title = models.CharField(max_length=255, verbose_name="Media Title")
	slug = models.SlugField(max_length=255, unique=True)
	text = models.CharField(max_length=40000, verbose_name="Media Description")
	email_text = models.CharField(max_length=10000, blank=True, null=True, verbose_name="Email Message Text")
	author = models.ForeignKey(User, limit_choices_to={'is_staff': True})
	byline = models.CharField(max_length=100, blank=True, null=True)
	is_published = models.BooleanField(default=False, verbose_name="Publish Media")
	send_now = models.CharField(max_length=50, default=False, verbose_name="Send Email")
	created_on = models.DateTimeField(auto_now_add=True)
	publish_date = models.DateTimeField(default=datetime.datetime.now())
	objects = models.Manager()
	docfile = models.FileField(upload_to='docs/%Y/%m/%d/', blank=True, null=True, verbose_name="Upload Media File")
	tags = TaggableManager(blank=True)

	def __unicode__(self):
		return self.title
	
	def save(self, *args, **kwargs):
		if not self.slug:
			y = self.publish_date.strftime("%Y")
			m = self.publish_date.strftime("%b").lower()
			d = self.publish_date.strftime("%d")
			self.slug = slugify(self.title) + "-" + d  + "-" + m  + "-" + y
		super(MediaItem, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('media_detail', kwargs={'slug': self.slug})


class PublishedArticlesManager(models.Manager):
	
	def get_query_set(self):
		return super(PublishedArticlesManager, self).get_query_set().filter(is_published=True)


class Article(models.Model):
	"""Represents a story article"""
	
	title = models.CharField(max_length=255, verbose_name="Headline")
	slug = models.SlugField(max_length=255, unique=True)
	text = models.CharField(max_length=40000, verbose_name="Story Text")
	email_text = models.CharField(max_length=10000, blank=True, null=True, verbose_name="Email Message Text")
	author = models.ForeignKey(User, limit_choices_to={'is_staff': True})
	byline = models.CharField(max_length=100, blank=True, null=True)
	is_published = models.BooleanField(default=False, verbose_name="Publish Story")
	send_now = models.CharField(max_length=50, default=False, verbose_name="Send Email")
	created_on = models.DateTimeField(auto_now_add=True)
	publish_date = models.DateTimeField(default=datetime.datetime.now())
	objects = models.Manager()
	published = PublishedArticlesManager()
	docfile = models.FileField(upload_to='docs/%Y/%m/%d/', blank=True, null=True, verbose_name="Add Attachment")
	mediaitems = models.ManyToManyField(MediaItem, blank=True, null=True)
	tags = TaggableManager(blank=True)

	def __unicode__(self):
		return self.title
	
	def save(self, *args, **kwargs):
		if not self.slug:
			y = self.publish_date.strftime("%Y")
			m = self.publish_date.strftime("%b").lower()
			d = self.publish_date.strftime("%d")
			self.slug = slugify(self.title) + "-" + d  + "-" + m  + "-" + y
		super(Article, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('story_article_detail', kwargs={'slug': self.slug})