from apps.profiles.models import Poll, Choice, Editor, Reporter, Client
from django.contrib import admin
from django.contrib.admin import site, ModelAdmin
from django.contrib.auth.models import User


class EditorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')

class ReporterAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')

class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    

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
# admin.site.unregister(User)
admin.site.register(Editor, EditorAdmin)
admin.site.register(Reporter, ReporterAdmin)
admin.site.register(Client, ClientAdmin)
