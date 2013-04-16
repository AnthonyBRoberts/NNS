from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import Context, RequestContext, loader
from apps.profiles.models import Editor, Reporter, Client
from forms import ClientForm

def client_index(request):
    """
    Client Index View, a list of all clients
    """
    client_list = Client.objects.all().order_by('city')
    return render_to_response('profiles/client_index.html',
                              {'client_list': client_list})

def client_details(request, client_id):
    """
    Client Details View, a list of all client details for given client_id
    """
    client_info = get_object_or_404(Client, pk=client_id)
    print "client_info"
    if request.method == 'POST':
        client_form = ClientForm(request.POST or None, instance=client_info)
        print "client_info"
        if client_form.is_valid():
            client_info = client_form.save()
            return HttpResponseRedirect('/profiles/clients/%s' % client_id)
    else:
        client_form = ClientForm(request.POST, instance=client_info)
        
    return render_to_response('profiles/client_detail.html',
                              {'client_form': client_form, 'client_info': client_info,},
                              context_instance=RequestContext(request))
    
"""
def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    t = loader.get_template('polls/index.html')
    c = Context({
        'latest_poll_list': latest_poll_list,
    })
    return HttpResponse(t.render(c))


def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    return render_to_response('polls/index.html',
                              {'latest_poll_list': latest_poll_list})

def detail(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('polls/detail.html', {'poll': p},
                              context_instance=RequestContext(request))

def results(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('polls/results.html', {'poll': p},
                              context_instance=RequestContext(request))

def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)    
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render_to_response('polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        }, context_instance=RequestContext(request))
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('poll_results', args=(p.id,)))
"""
