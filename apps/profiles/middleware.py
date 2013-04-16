from django.contrib.auth.models import User
from apps.polls.models import Editor, Reporter, Client

class RequestMiddleWare(object):
    """docstring for """
    def process_request(self,request):
        if isEditor(request.user):
            request.user.userprofile = Editor.objects.get(user=request.user.id)
        elif isReporter(request.user):
            request.user.userprofile = Reporter.objects.get(user=request.user.id)
        elif isClient(request.user):
            request.user.userprofile = Client.objects.get(user=request.user.id)  
        return None   

def isEditor(user):
    return Editor.objects.filter(user=user.id).exists()

def isReporter(user):
    return Reporter.objects.filter(user=user.id).exists()

def isClient(user):
    return Client.objects.filter(user=user.id).exists()
