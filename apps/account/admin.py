from django.contrib import admin
from django.contrib.admin import site, ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from models import *

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'user profiles'
    fieldsets = (
        ('Staff information', {
            'fields': (('user_type', 'can_publish'), 'byline', 'bio'),
        }),
        ('Client information', {
            'classes': ('collapse',),
            'fields': (('pub_name', 'pub_type'),
                       'pub_area', 'phone', 'address', 'city',
                       'state', 'zipcode', 'website',
                       ('facebook', 'twitter'), 'about'),
        }),
    )

class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )

    
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

