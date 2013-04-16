from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to, direct_to_template
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', direct_to_template, { "template" : "welcome.html"}),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/django-ses/', include('django_ses.urls')),
    url(r'^examples/', include('apps.examples.urls')),
    url(r'^profiles/', include('apps.profiles.urls')),
    url(r'^pastebin/', include('apps.pastebin.urls')),
    url(r'^blog/', include('apps.blog.urls')),
    url(r'^wiki/', include('apps.wiki.urls')),
    # url(r'^nns/', include('apps.nns.urls')),
)

if getattr(settings,"DEBUG"):
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
