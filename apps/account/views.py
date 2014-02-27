"""
Views for creating, editing and viewing site-specific user profiles.

"""
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render_to_response
from django.template import RequestContext
import django.contrib.auth.decorators
import django.contrib.auth.models
import django.core.exceptions
import django.core.urlresolvers
import django.http
import django.shortcuts
import django.template
import django.views.generic.list
from account.models import *
from account.signals import user_activated

def unsubscribe(request, form_class, success_url=None,
                template_name='profiles/unsubscribe.html'):
    try:
        profile_obj = request.user.get_profile()
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('profiles_create_profile'))
    
    if success_url is None:
        success_url = reverse('profiles_profile_detail',
                              kwargs={'username': request.user.username})
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES, instance=profile_obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(success_url)
    else:
        form = form_class(instance=profile_obj)
    return render_to_response(template_name,
                              {'form': form,
                              'profile': profile_obj, })
unsubscribe = login_required(unsubscribe)


def client_index(request):
    """
    Client index view, a list of all clients
    """
    client_list = UserProfile.objects.filter(user_type='Client').order_by('pub_name')
    paginator = Paginator(client_list, 10)
    page = request.GET.get('page')
    try:
        show_lines = paginator.page(page)
    except PageNotAnInteger:
        show_lines = paginator.page(1)
    except EmptyPage:
        show_lines = paginator.page(paginator.num_pages)
    return render_to_response('profiles/profile_list.html', RequestContext(request, {
        'lines': show_lines,
    }))


def reporter_index(request):
    """
    Reporter index view, a list of all clients
    """
    reporter_list = UserProfile.objects.filter(user_type='Reporter')
    paginator = Paginator(reporter_list, 10)
    page = request.GET.get('page')
    try:
        show_lines = paginator.page(page)
    except PageNotAnInteger:
        show_lines = paginator.page(1)
    except EmptyPage:
        show_lines = paginator.page(paginator.num_pages)
    return render_to_response('profiles/reporter_list.html', RequestContext(request, {
        'lines': show_lines,
    }))


def editor_index(request):
    """
    Editor index view, a list of all clients
    """
    editor_list = UserProfile.objects.filter(user_type='Editor')
    paginator = Paginator(editor_list, 10)
    page = request.GET.get('page')
    try:
        show_lines = paginator.page(page)
    except PageNotAnInteger:
        show_lines = paginator.page(1)
    except EmptyPage:
        show_lines = paginator.page(paginator.num_pages)
    return render_to_response('profiles/editor_list.html', RequestContext(request, {
        'lines': show_lines,
    }))