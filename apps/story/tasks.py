import logging
from celery import task
from django.core.servers.basehttp import FileWrapper
from django.core.files import File
from django.db.models import Q
from apps.account.models import UserProfile
from story.email import EMail, log_email
import datetime
import time

@task(name='send-email')
def send_published_article(bc_only, sender, subject, byline, email_text, story_text, attachment=None):
    """
    Task for emailing published articles.
    Runs when an article is saved and both is_published & send_now==True
    """
    recipients = []
    date_string = time.strftime("%Y-%m-%d-%H-%M")
    logFile = open('static/email_logs/sent_emails-' + date_string + '.txt', 'w')
    logFile.write("Recipients for " + date_string + ":\n")
    logFile.close()
    for profile in UserProfile.objects.filter(user_type = 'Editor'):
        recipients.append(profile.user.email)
    for profile in UserProfile.objects.filter(user_type = 'Reporter'):        
        recipients.append(profile.user.email)
    if bc_only:
        for profile in UserProfile.objects.filter(Q(user_type = 'Client') & (Q(pub_type = 'Radio') | Q(pub_type = 'Television'))):
            recipients.append(profile.user.email)
    else:
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
        log_email(r, date_string)
        time.sleep(1)  
    


