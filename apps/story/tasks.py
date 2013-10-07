import logging
from celery import task
from django.core.servers.basehttp import FileWrapper
from apps.account.models import UserProfile
from story.email import EMail
import time

@task(name='send-email')
def send_published_article(sender, subject, byline, email_text, story_text, attachment=None):
    """
    Task for emailing published articles.
    Runs when an article is saved and both is_published & send_now==True
    """
    recipients = []
    for profile in UserProfile.objects.filter(user_type = 'Editor'):
        recipients.append(profile.user.email)
    for profile in UserProfile.objects.filter(user_type = 'Reporter'):        
        recipients.append(profile.user.email)
    for profile in UserProfile.objects.filter(user_type = 'Client'):
        recipients.append(profile.user.email)
    for r in recipients:
        bcc = ['nns.aroberts@gmail.com',]
        email = EMail(subject, r, bcc)
        ctx = {'subject': subject, 'story_text': story_text, 'email_text': email_text, 'byline': byline}
        email.text('../templates/templated_email/emaila.txt', ctx)
        email.html('../templates/templated_email/emaila.html', ctx)  
        if attachment:
            email.add_attachment(attachment) 
        email.send()
        time.sleep(1)
 
@task()
def report_errors():
    logging.error("reporting errors")
