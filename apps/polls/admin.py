from apps.polls.models import Poll, Choice, Editor, Reporter, Client
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class EditorInline(admin.StackedInline):
    model = Editor
    verbose_name_plural = 'editor profile'

class EditorAdmin(UserAdmin):
    inlines = (EditorInline, )
    
class ReporterInline(admin.StackedInline):
    model = Reporter
    verbose_name_plural = 'reporter profile'

class ReporterAdmin(UserAdmin):
    inlines = (ReporterInline, )

class ClientInline(admin.StackedInline):
    model = Client
    verbose_name_plural = 'client profile'

class ClientAdmin(UserAdmin):
    inlines = (ClientInline, )

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question']
    date_hierarchy = 'pub_date'


admin.site.register(Poll, PollAdmin)
admin.site.unregister(User)
admin.site.register(User, EditorAdmin)
