from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView
from apps.story.models import Article, MediaItem

urlpatterns = patterns('',
	url(r'^$', 
		'story.views.story_index',
		name='story_article_index'),
	url(r'^inprogress/$',
		'story.views.inprogress_index',
		name='inprogress_list'),
	url(r'^article/(?P<slug>[-\w]+)$', 
		DetailView.as_view(queryset=Article.objects.all()),
		name='story_article_detail'
	),
	url(r'^add/article$',
		'story.views.add_article',
		name='story_article_add'),
	url(r'^edit/article/(?P<slug>[-\w]+)$',
		'story.views.edit_article',
		name='story_article_edit'),
	url(r'^media/$',
		'story.views.media_index',
		name='media_list'),
	url(r'^media/inprogress$',
		'story.views.media_inprogress_index',
		name='media_inprogress_list'),
	url(r'^media/(?P<slug>[-\w]+)$', 
		DetailView.as_view(queryset=MediaItem.objects.all()),
		name='media_detail'
	),
	url(r'^add/media$',
		'story.views.add_media',
		name='media_add'),
	url(r'^edit/media/(?P<slug>[-\w]+)$',
		'story.views.edit_media',
		name='media_edit'),
)