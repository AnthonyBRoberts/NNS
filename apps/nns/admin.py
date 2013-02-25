from apps.nns.models import Content, Note
from django.contrib import admin




class ContentAdmin(admin.ModelAdmin):
    
    """
    General Story Editor, needs TinyMCE editor or equivalent,
    
    Fields: Text Editor, Photos, YouTube Video links, files,
    titles, by-lines, photo cut lines, addition text fields, 
    tags, reporter notes, editor notes, distribution list,
    date created, date modified, date published, date re-published
    
    fieldsets = [
        (None,               {'fields': ['title', 'byline']}),
        ('Date information', {'fields': ['text']}),
    ]
    list_display = ('title', 'byline', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question']
    date_hierarchy = 'pub_date'

    """

class NotesAdmin(admin.modelAdmin):

    """
    Fields: Client, Reporter (both Foreign Key and Many to Many)
    text, tags, date created, date modified.
    """


admin.site.register(Content) #, ContentAdmin)
admin.site.register(Note) #, NoteAdmin)


