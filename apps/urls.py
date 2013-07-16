from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib import admin
from registration.views import register
from account.forms import *
from account.models import *
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name= "welcome_content.html")),
    url(r'^accounts/register/$',
        register,
        {'backend': 'registration.backends.simple.SimpleBackend',
        'template_name': 'registration/registration_form.html',
        'form_class': EmailRegistrationForm,
        'success_url': getattr(
            settings, 'REGISTRATION_EMAIL_REGISTER_SUCCESS_URL', None),
        },
        name='registration_register', 
    ),
    url(r'^accounts/', include('registration_email.backends.default.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/django-ses/', include('django_ses.urls')),
    url(r'^story/', include('apps.story.urls')),
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
    url(r'^profiles/', include('apps.account.urls')),
    (r'^tinymce/', include('tinymce.urls')),
)

if getattr(settings,"DEBUG"):
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
