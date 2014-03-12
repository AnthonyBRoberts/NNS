from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from account.models import *


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