from django.conf.urls.defaults import *
from models import Post

urlpatterns = patterns('',
    url(r'^post/(?P<slug>[-\w]+)$', 
        'blog.views.view_post',
        name='blog_post_detail'),
    url(r'^add/post$', 
        'blog.views.add_post', 
        name='blog_add_post'),
    url(r'^archive/month/(?P<year>\d+)/(?P<month>\w+)$',
        'django.views.generic.date_based.archive_month',
        {
            'queryset': Post.objects.all(), 
            'date_field': 'created_on',
        },
        name='blog_archive_month',
       ),
    url(r'^archive/week/(?P<year>\d+)/(?P<week>\d+)$',
        'django.views.generic.date_based.archive_week',
        {
            'queryset': Post.objects.all(), 
            'date_field': 'created_on',
        },
        name='blog_archive_week',
       ),
    url(r'$', 'django.views.generic.list_detail.object_list',
        { 'queryset': Post.objects.all() }, name='blog_post_list'),
)
