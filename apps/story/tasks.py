from django.core.mail import send_mail
from celery import task
import logging
from apps.profiles.models import Client

@task(name='send-email')
def send_published_article(sender, subject, body):
    """
    Task for emailing published articles.
    Runs when an article is saved and is_published==True
    """
    for client in Client.objects.all():
        recipient = client.email
        send_mail(subject, body, sender, [recipient], fail_silently=False)

@task()
def report_errors():
    logging.error("reporting errors")
