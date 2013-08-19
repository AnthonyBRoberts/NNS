from django.contrib import admin
from django.forms import *
from django.forms import ModelForm
from django.contrib.admin import ModelAdmin
from suit_redactor.widgets import RedactorWidget
from django.db.models import *
from models import Article
from tinymce.widgets import TinyMCE
from taggit.models import Tag, TaggedItem

class TagInline(admin.TabularInline):
    model = Tag

class ArticleAdminForm(ModelForm):
    class Meta:
        widgets = {
            'email_text': RedactorWidget(editor_options={'lang': 'en'}),
            'text': RedactorWidget(editor_options={'lang': 'en'}),
        }
        model = Article
    
class ArticleAdmin(ModelAdmin):
    form = ArticleAdminForm
    list_display = ('title', 'is_published', 'docfile')
    list_filter = ['author', 'is_published', ]
    search_fields = ['title', 'author',]
    date_hierarchy = 'publish_date'
    fieldsets = [
        (None, {'classes': ['edit'], 
            'fields': (('title', 'slug'), 'author',
                       ('is_published', 'publish_date', 'send_now'),
                       'docfile', 'text', 'email_text'),
            }),
    ]
    #inlines = (TagInline, )

admin.site.register(Article, ArticleAdmin)



