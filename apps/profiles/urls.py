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
)


