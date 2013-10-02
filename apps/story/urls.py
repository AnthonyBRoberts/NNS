from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView
from apps.story.models import Article

urlpatterns = patterns('',
    url(r'^$', 
        'story.views.story_index',
        name='story_article_index'),
    url(r'^inprogress/$',
        'story.views.inprogress_index',
        name='inprogress_list'),
    url(r'^article/(?P<slug>[-\w]+)$', 
        'django.views.generic.list_detail.object_detail',
        {
            'queryset': Article.objects.all(),
        },
        name='story_article_detail'),
    url(r'^add/article$',
        'story.views.add_article',
        name='story_article_add'),
    url(r'^edit/article/(?P<slug>[-\w]+)$',
        'story.views.edit_article',
        name='story_article_edit'),
)
