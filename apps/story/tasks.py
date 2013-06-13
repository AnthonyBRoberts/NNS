import logging
from celery import task
from django.core.mail.message import EmailMessage
from django.core.servers.basehttp import FileWrapper
from django.core.files.storage import default_storage
from django.http import HttpResponse
from apps.account.models import UserProfile
from templated_email import get_templated_mail

@task(name='send-email')
def send_published_article(username, full_name, signup_date, sender, subject, email_text, story_text, attachment=None):
    """
    Task for emailing published articles.
    Runs when an article is saved and is_published==True
    """
    recipients = []
    reporters = []
    for profile in UserProfile.objects.all():
        if profile.user_type == 'Client':
            recipients.append(profile.user.email)
        if profile.user_type == 'Reporter':
            reporters.append(profile.user.email)
    #email = EmailMessage(subject, body, sender, recipients)
    email = get_templated_mail(
        template_name='welcome',
        from_email=sender,
        to=['nns.aroberts@gmail.com'],
        context={
            'username':username,
            'full_name':full_name,
            'signup_date':signup_date,
            'subject':subject,
            'email_text':email_text,
            'story_text':story_text
        },
        # Optional:
        cc=reporters,
        bcc=recipients,
        # headers={'My-Custom-Header':'Custom Value'},
        # template_prefix="my_emails/",
        # template_suffix="email",
)
    if attachment != None:
        try:
            docfile = default_storage.open(attachment.name, 'r')
            if docfile:
                email.attach(docfile.name, docfile.read())
            else:
                pass
        except:
            pass
    email.send()
 
@task()
def report_errors():
    logging.error("reporting errors")
