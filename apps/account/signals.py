from models import *
from registration.signals import *

def create_user_profile(sender, instance, request, **kwargs):
    """
    When user is created also create a matching profile.
    """
    request, instance = kwargs['request'], kwargs['user']
    
    try:
        user_type = request.POST['user_type'].lower()
        if user_type == "client":  #user .lower for case insensitive comparison 
            Client(user = instance).save()
        elif user_type == "reporter":
            Reporter(user = instance).save()
        elif user_type == "editor":
            Editor(user = instance).save()
        else:
            UserProfile(user = instance).save()  #Default create - might want to raise error instead 
    except KeyError:
        UserProfile(user = instance).save()  #Default create just a profile

user_registered.connect(create_user_profile)
