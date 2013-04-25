from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from apps.profiles.models import Editor, Reporter, Client

urlpatterns = patterns('',
    url(r'^clients/$',
        ListView.as_view(
            queryset=Client.objects.order_by('-city'),
            context_object_name='clients_list',
            template_name='profiles/client_index.html')
        ),
    url(r'^clients/(?P<client_id>\d+)/$',
        'profiles.views.client_details',
        name='client_detail'),
    url(r'^clients/add$',
        'profiles.views.add_client',
        name='client_add'),
    url(r'^reporters/$',
        ListView.as_view(
            queryset=Reporter.objects.order_by('first_name'),
            context_object_name='reporter_list',
            template_name='profiles/reporter_index.html')
        ),
    url(r'^reporters/(?P<reporter_id>\d+)/$',
        'profiles.views.reporter_details',
        name='reporter_detail'),
    url(r'^reporters/add$',
        'profiles.views.add_reporter',
        name='reporter_add'),
    url(r'^editors/$',
        ListView.as_view(
            queryset=Editor.objects.order_by('first_name'),
            context_object_name='editor_list',
            template_name='profiles/editor_index.html')
        ),
    url(r'^editors/(?P<editor_id>\d+)/$',
        'profiles.views.editor_details',
        name='editor_detail'),
    url(r'^editors/add$',
        'profiles.views.add_editor',
        name='editor_add'),
)


