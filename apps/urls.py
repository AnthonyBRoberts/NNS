from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib import admin
from account.forms import *
from account.models import *
#from profiles import views
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^static/js/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
    }),
    url(r'^$', TemplateView.as_view(template_name= "welcome.html")),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/django-ses/', include('django_ses.urls')),
    url(r'^story/', include('apps.story.urls')),
    url(r'^profile/(?P<username>\w+)/$', 'profiles.views.profile_detail', name='profiles_profile_detail'),
    url(r'^reporters/', 'profiles.views.profile_list',
        {
            'template_name': 'profiles/reporter_list.html'
        },
        name='profiles_reporter_list'),
    url(r'^editors/', 'profiles.views.profile_list',
        {
            'template_name': 'profiles/editor_list.html'
        },
        name='profiles_editor_list'),
    url('^profiles/create/client', 'profiles.views.create_profile',
        {
          'form_class': ClientForm,
        },
        name='create_client_profile'),
    url('^profiles/edit/client/', 'profiles.views.edit_profile',
        {
            'form_class': ClientForm,
        },
        name='edit_client_profile'),
    (r'^profiles/', include('profiles.urls')),
    (r'^tinymce/', include('tinymce.urls')),
)

if getattr(settings,"DEBUG"):
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
