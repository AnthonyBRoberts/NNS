import logging
from celery import task
from django.core.mail.message import EmailMessage
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
from apps.account.models import Client

@task(name='send-email')
def send_published_article(sender, subject, body, attachment=None):
    """
    Task for emailing published articles.
    Runs when an article is saved and is_published==True
    """
    #recipients = []
    for client in Client.objects.all():
        #recipients.append(client.email)
        recipient = client.user.email
        email = EmailMessage(subject, body, sender, [recipient])
        if attachment != None:
            try:
                for (k, v) in attachment:
                    email.attach(v.name, v.read())
            except ValueError:
                email.attach(attachment.name, attachment.read())
        email.send()

@task()
def report_errors():
    logging.error("reporting errors")
