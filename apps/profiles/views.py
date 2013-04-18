from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import Context, RequestContext, loader
from apps.profiles.models import Editor, Reporter, Client
from forms import ClientForm

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
            client_info = client_form.save()
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
        client_info.city = 'request.method == POST'
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
    
