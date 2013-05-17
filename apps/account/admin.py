from django.contrib import admin
from django.contrib.admin import site, ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from models import *


class ClientInline(admin.StackedInline):
    model = Client
    can_delete = False
    verbose_name_plural = 'client'

class ReporterInline(admin.StackedInline):
    model = Reporter
    can_delete = False
    verbose_name_plural = 'reporter'

class EditorInline(admin.StackedInline):
    model = Editor
    can_delete = False
    verbose_name_plural = 'editor'

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'user profile'

class UserAdmin(UserAdmin):
    """
    If the user displayed is superuser, UserAdmin needs EditorInline
    If the user displayed is staff, UserAdmin needs ReporterInline
    If the user displayed is authenticated, UserAdmin needs ClientInline
    Else Admin needs UserProfileInline
    
    if User.is_superuser:
        inlines = (EditorInline, )
    elif user.is_staff:
        inlines = (ReporterInline, )
    elif user.is_authenticated:
        inlines = (ClientInline, )
    else:
        inline = (UserProfileInline, )
    """

    
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Client)
admin.site.register(Reporter)
admin.site.register(Editor)

#class EditorAdmin(admin.ModelAdmin):
#    list_display = ('first_name', 'last_name', 'email')

#class ReporterAdmin(admin.ModelAdmin):
#    list_display = ('first_name', 'last_name', 'email')

#class ClientAdmin(admin.ModelAdmin):
#    list_display = ('first_name', 'last_name', 'email')
    
#class ProfileAdmin(admin.ModelAdmin):
    #list_display = ('first_name', 'last_name', 'email')


#admin.site.register(Editor)#, EditorAdmin)
#admin.site.register(Reporter)#, ReporterAdmin)
#admin.site.register(Client)#, ClientAdmin)
