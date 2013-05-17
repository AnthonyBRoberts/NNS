from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView
from apps.story.models import Article

urlpatterns = patterns('',
    url(r'^$', 
        'django.views.generic.list_detail.object_list',
        {
            'queryset': Article.objects.all(),
        },
        name='story_article_index'),
    url(r'^inprogress/$',
        ListView.as_view(
            queryset=Article.objects.filter(is_published=False),
            context_object_name='inprogress_list',
            template_name='story/article_inprogress_list.html')
        ),
    url(r'^article/(?P<slug>[-\w]+)$', 
        'django.views.generic.list_detail.object_detail',
        {
            'queryset': Article.objects.all(),
        },
        name='story_article_detail'),
    url(r'^history/(?P<slug>[-\w]+)$',
        'story.views.article_history',
        name='story_article_history'),
    url(r'^add/article$',
        'story.views.add_article',
        name='story_article_add'),
    url(r'^edit/article/(?P<slug>[-\w]+)$',
        'story.views.edit_article',
        name='story_article_edit'),
)
