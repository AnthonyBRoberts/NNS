from django.core.mail.message import EmailMessage
from celery import task
import logging
from apps.profiles.models import Client

@task(name='send-email')
def send_published_article(sender, subject, body, attachment):
    """
    Task for emailing published articles.
    Runs when an article is saved and is_published==True
    """
    recipients = []
    for client in Client.objects.all():
        recipients.append(client.email)
    email = EmailMessage(subject, body, sender, [recipients])
    email.attach_file(attachment)
    email.send()

@task()
def report_errors():
    logging.error("reporting errors")
