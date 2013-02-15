from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'apps.polls.views.index', name='index'),
    url(r'^(?P<poll_id>\d+)/$', 'apps.polls.views.detail', name='detail'),
    url(r'^(?P<poll_id>\d+)/results/$', 'results'),
    url(r'^(?P<poll_id>\d+)/vote/$', 'vote'),
)
