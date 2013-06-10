from django.contrib import admin
from django.forms import *
from django.db.models import *
from models import Article, Edit
from tinymce.widgets import TinyMCE

class EditInline(admin.TabularInline):
    model = Edit

class ArticleAdminForm(forms.ModelForm):
    text = forms.CharField(widget=TinyMCE())
    class Meta:
        model = Article
    
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = ('title', 'author', 'is_published', 'docfile')
    list_filter = ['title', 'author', 'is_published', ]
    search_fields = ['title', 'author',]
    date_hierarchy = 'publish_date'
    fieldsets = [
        (None, {'classes': ['edit'], 
            'fields': (('title', 'slug'), 'author',
                       ('is_published', 'publish_date'),
                       'docfile', 'text'),
            }),
    ]
    #inlines = [EditInline]

admin.site.register(Article, ArticleAdmin)

