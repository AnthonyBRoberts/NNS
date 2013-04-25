from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from tinymce import models as tinymce_models
import datetime

class PublishedArticlesManager(models.Manager):
    
    def get_query_set(self):
        return super(PublishedArticlesManager, self).get_query_set().filter(is_published=True)

class Article(models.Model):
    """Represents a story article"""
    
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, unique=True)
    text = tinymce_models.HTMLField()
    author = models.ForeignKey(User)
    is_published = models.BooleanField(default=False, verbose_name="Publish?")
    created_on = models.DateTimeField(auto_now_add=True)
    publish_date = models.DateTimeField(default=datetime.datetime.now())
    objects = models.Manager()
    published = PublishedArticlesManager()
    docfile = models.FileField(upload_to='docs/%Y/%m/%d/', blank=True, null=True)

    def __unicode__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    @models.permalink 
    def get_absolute_url(self):
        return ('story_article_detail', (), { 'slug': self.slug })

class Edit(models.Model):
    """Stores an edit session"""
    
    article = models.ForeignKey(Article)
    editor = models.ForeignKey(User)
    edited_on = models.DateTimeField(auto_now_add=True)
    summary = models.CharField(max_length=100)

    class Meta:
        ordering = ['-edited_on']

    def __unicode__(self):
        return "%s - %s - %s" %(self.summary, self.editor, self.edited_on)
    
    @models.permalink 
    def get_absolute_url(self):
        return ('story_edit_detail', self.id)