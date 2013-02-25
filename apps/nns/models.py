from django.db import models

class Content(models.Model):
    
    """
    A NNS Content Object
    Fields: Stories, Photos, YouTube Video links, files,
    titles, by-lines, photo cut lines, addition text fields, 
    tags, reporter notes, editor notes, distribution list,
    date created, date modified, date published, date re-published

    I should sub-class each type of content.
    
    """

    title = models.CharField(max_length=100)
    def __unicode__(self):
        return self.title
    bodytext = models.CharField(max_length=1000)
    byline = models.CharField(max_length=100)
    date_created = models.DateField('date created')
    date_published = models.DateField('date published')

class EditorProfile(models.Model):
    
    """
    An Editor User Profile object.
    Default superuser, can be set to not superuser?
    Fields: phone, notes,

    Has access to special methods of Content objects:
    date published, date re-published  
    """
    
class ReporterProfile(models.Model):
    
    """
    A Reporter User Profile object.
    Fields: By-line, phone #, notes, publish logs, 
    """

class ClientProfile(models.Model):
    
    """
    A Client User Profile object.
    Fields: Address, Phone #, type?, website, social media,
    contact person, additional contacts, 

    Should sub-class Newspaper, Radio, TV, or make this a field of name "type"

    """

class Note(models.Model):

    """
    A Note object
    Fields: Client, Reporter, both Foreign Key and Many to Many,
    text, tags, date created, date modified.
    """

    
