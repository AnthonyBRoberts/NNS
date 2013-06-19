import logging
from celery import task
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail.message import EmailMessage, EmailMultiAlternatives
from django.core.servers.basehttp import FileWrapper
from django.core.files.storage import default_storage
from django.http import HttpResponse
from apps.account.models import UserProfile
from templated_email import get_templated_mail

class EMail(object):
    """
    A wrapper around Django's EmailMultiAlternatives
    that renders txt and html templates.
    Example Usage:
    >>> email = Email(to='oz@example.com', subject='A great non-spammy email!')
    >>> ctx = {'username': 'Oz Katz'}
    >>> email.text('templates/email.txt', ctx)
    >>> email.html('templates/email.html', ctx)  # Optional
    >>> email.send()
    >>>
    """
    def __init__(self, subject, to, cc, bcc):
        self.subject = subject
        self.to = to
        self.cc = cc
        self.bcc = bcc
        self._html = None
        self._text = None
        self._attachment = None

    def _render(self, template, context):
        return render_to_string(template, context)

    def html(self, template, context):
        self._html = self._render(template, context)

    def text(self, template, context):
        self._text = self._render(template, context)

    def add_attachment(self, attachment):
        self._attachment = default_storage.open(attachment.name, 'r')
        
    def send(self, from_addr=None, fail_silently=False):
        if isinstance(self.to, basestring):
            self.to = [self.to]
        if not from_addr:
            from_addr = getattr(settings, 'DEFAULT_FROM_EMAIL')
        msg = EmailMultiAlternatives(
            self.subject,
            self._text,
            from_addr,
            to=self.to,
            cc=self.cc,
            bcc=self.bcc
        )
        if self._html:
            msg.attach_alternative(self._html, 'text/html')
        if self._attachment:
            msg.attach(self._attachment.name, self._attachment.read())
        msg.send()

@task(name='send-email')
def send_published_article(sender, subject, email_text, story_text, attachment=None):
    """
    Task for emailing published articles.
    Runs when an article is saved and is_published==True
    """
    recipients = []
    reporters = []
    editors = []
    for profile in UserProfile.objects.all():
        if profile.user_type == 'Client':
            recipients.append(profile.user.email)
        if profile.user_type == 'Reporter':
            reporters.append(profile.user.email)
        if profile.user_type == 'Editor':
            editors.append(profile.user.email)
    email = EMail(subject, to=editors, cc=reporters, bcc=recipients)

    ctx = {'story_text': story_text, 'email_text': email_text}
    email.text('../templates/templated_email/emaila.txt', ctx)
    email.html('../templates/templated_email/emaila.html', ctx)  # Optional
    if attachment != None:
        email.add_attachment(attachment) # Optional
    email.send()
 
@task()
def report_errors():
    logging.error("reporting errors")
