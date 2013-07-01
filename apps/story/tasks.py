import logging
from celery import task
from django.core.servers.basehttp import FileWrapper
from apps.account.models import UserProfile
from story.email import EMail

@task(name='send-email')
def send_published_article(sender, subject, byline, email_text, story_text, attachment=None):
    """
    Task for emailing published articles.
    Runs when an article is saved and is_published==True
    """
    clients = []
    reporters = []
    editors = []
    for profile in UserProfile.objects.all():
        if profile.user_type == 'Client':
            clients.append(profile.user.email)
        elif profile.user_type == 'Reporter':
            reporters.append(profile.user.email)
        elif profile.user_type == 'Editor':
            editors.append(profile.user.email)
    email = EMail(subject, editors, reporters, clients)
    ctx = {'subject': subject, 'story_text': story_text, 'email_text': email_text, 'byline': byline}
    email.text('../templates/templated_email/emaila.txt', ctx)
    email.html('../templates/templated_email/emaila.html', ctx)  
    if attachment:
        email.add_attachment(attachment) 
    email.send()
 
@task()
def report_errors():
    logging.error("reporting errors")
