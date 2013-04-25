from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import Context, RequestContext, loader
from apps.profiles.models import Editor, Reporter, Client
from apps.story.models import Article, Edit
from forms import ClientForm, ReporterForm, EditorForm

@login_required 
def client_index(request):
    """
    Client Index View, a list of all clients
    """
    client_list = Client.objects.all().order_by('city')
    return render_to_response('profiles/client_index.html',
                              {'client_list': client_list})

@login_required
def add_client(request):
    """
    Add new client, a blank client form
    """
    if request.method == 'POST':
        client_form = ClientForm(request.POST)
        if client_form.is_valid():
            client_info = client_form.save(commit=False)
            client_info.email = client_info.username
            client_info.save()
            msg = "Client saved successfully"
            messages.success(request, msg, fail_silently=True)
            return HttpResponseRedirect('/profiles/clients/%s' % client_info.id)
    else:
        client_form = ClientForm()
    return render_to_response('profiles/client_detail.html',
                              {
                                  'client_form': client_form,
                              },
                              context_instance=RequestContext(request))
    
@login_required 
def client_details(request, client_id):
    """
    Client Details View, a list of all client details for given client_id
    """
    client_info = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        client_form = ClientForm(request.POST or None, instance=client_info)
        if client_form.is_valid():
            client_info = client_form.save()
            return HttpResponseRedirect('/profiles/clients/%s' % client_id)
    else:
        client_form = ClientForm(request.POST or None, instance=client_info)
        
    return render_to_response('profiles/client_detail.html',
                              {
                                  'client_form': client_form,
                                  'client_info': client_info,
                              },
                              context_instance=RequestContext(request))

@login_required 
def reporter_index(request):
    """
    Reporter Index View, a list of all reporters
    """
    reporter_list = Reporter.objects.all().order_by('first_name')
    return render_to_response('profiles/reporter_index.html',
                              {'reporter_list': reporter_list})

@login_required
def add_reporter(request):
    """
    Add new reporter, a blank reporter form
    """
    if request.method == 'POST':
        reporter_form = ReporterForm(request.POST)
        if reporter_form.is_valid():
            reporter_info = reporter_form.save(commit=False)
            reporter_info.is_staff = True
            reporter_info.save()
            content_type = ContentType.objects.get_for_model(Article)
            perm1 = Permission.objects.get(content_type=content_type, codename='add_article')
            perm2 = Permission.objects.get(content_type=content_type, codename='change_article')
            perm3 = Permission.objects.get(content_type=content_type, codename='delete_article')
            content_type2 = ContentType.objects.get_for_model(Edit)
            perm4 = Permission.objects.get(content_type=content_type2, codename='add_edit')
            perm5 = Permission.objects.get(content_type=content_type2, codename='change_edit')
            perm6 = Permission.objects.get(content_type=content_type2, codename='delete_edit')
            reporter_info.user_permissions.add(perm1, perm2, perm3, perm4, perm5, perm6)
            msg = "Reporter saved successfully"
            messages.success(request, msg, fail_silently=True)
            return HttpResponseRedirect('/profiles/reporters/%s' % reporter_info.id)
    else:
        reporter_form = ReporterForm()
    return render_to_response('profiles/reporter_detail.html',
                              {
                                  'reporter_form': reporter_form,
                              },
                              context_instance=RequestContext(request))

@login_required 
def reporter_details(request, reporter_id):
    """
    Reporter Details View, a list of all reporter details for given reporter_id
    """
    reporter_info = get_object_or_404(Reporter, id=reporter_id)
    if request.method == 'POST':
        reporter_form = ReporterForm(request.POST or None, instance=reporter_info)
        if reporter_form.is_valid():
            reporter_info = reporter_form.save()
            return HttpResponseRedirect('/profiles/reporters/%s' % reporter_id)
    else:
        reporter_form = ReporterForm(request.POST or None, instance=reporter_info)
        
    return render_to_response('profiles/reporter_detail.html',
                              {
                                  'reporter_form': reporter_form,
                                  'reporter_info': reporter_info,
                              },
                              context_instance=RequestContext(request))

@login_required 
def editor_index(request):
    """
    Editor Index View, a list of all editors
    """
    editor_list = Editor.objects.all().order_by('first_name')
    return render_to_response('profiles/editor_index.html',
                              {'reporter_list': reporter_list})

@login_required
def add_editor(request):
    """
    Add new editor, a blank editor form
    """
    if request.method == 'POST':
        editor_form = EditorForm(request.POST)
        if editor_form.is_valid():
            editor_info = editor_form.save(commit=False)
            editor_info.is_staff = True
            editor_info.is_superuser = True
            editor_info.save()
            msg = "Editor saved successfully"
            messages.success(request, msg, fail_silently=True)
            return HttpResponseRedirect('/profiles/editors/%s' % editor_info.id)
    else:
        editor_form = EditorForm()
    return render_to_response('profiles/editor_detail.html',
                              {
                                  'editor_form': editor_form,
                              },
                              context_instance=RequestContext(request))

@login_required 
def editor_details(request, editor_id):
    """
    Editor Details View, a list of all editor details for given reporter_id
    """
    editor_info = get_object_or_404(Editor, id=editor_id)
    if request.method == 'POST':
        editor_form = EditorForm(request.POST or None, instance=editor_info)
        if editor_form.is_valid():
            editor_info = editor_form.save()
            return HttpResponseRedirect('/profiles/editors/%s' % editor_id)
    else:
        editor_form = EditorForm(request.POST or None, instance=editor_info)
        
    return render_to_response('profiles/editor_detail.html',
                              {
                                  'editor_form': editor_form,
                                  'editor_info': editor_info,
                              },
                              context_instance=RequestContext(request))


