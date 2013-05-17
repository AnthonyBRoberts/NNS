from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib import admin
from account.forms import *
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
    url('^profiles/create/client', 'profiles.views.create_profile', {
        'form_class': ClientForm,
    },
        name='create_client_profile'),
    url('^profiles/create/reporter', 'profiles.views.create_profile', {
        'form_class': ReporterForm,
        'success_url':'/story',
    }),
    url('^profiles/create/editor', 'profiles.views.create_profile', {
        'form_class': EditorForm,
        'success_url':'/story',
    }),
    url('^profiles/edit/client/', 'profiles.views.edit_profile', {
        'form_class': ClientForm,
        'success_url':'/story',
    }),
    url('^profiles/edit/reporter', 'profiles.views.edit_profile', {
        'form_class': ReporterForm,
        'success_url':'/story',
    }),
    url('^profiles/edit/editor', 'profiles.views.edit_profile', {
        'form_class': EditorForm,
        'success_url':'/story',
    }),
    
    (r'^profiles/', include('profiles.urls')),
    (r'^tinymce/', include('tinymce.urls')),
)

if getattr(settings,"DEBUG"):
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
