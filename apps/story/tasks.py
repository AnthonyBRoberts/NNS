from celery import task
from story.email import EMail, log_email
from django.conf import settings
import logging
import datetime
import time
from apps.account.models import UserProfile


@task(name='email-batch')
def create_email_batch(date_string, sender, recipients, subject, byline, email_text, story_text, attachment=None):
    """
    Task for emailing published articles.
    Runs when an article is saved and both is_published & send_now==True
    """
    editors = []
    email_addresses = []
    for profile in UserProfile.objects.filter(user_type = 'Editor'):
        editors.append(profile.user.email)    
    for r in recipients:
        send_published_article.delay(date_string, sender, r, subject,
                                                        byline, email_text, story_text, attachment)
        email_addresses.append(r)
        time.sleep(2)
    report_subject = 'Email report for ' + date_string 
    story_title = subject
    email_report.delay(settings.DEFAULT_FROM_EMAIL, editors, report_subject, story_title, email_addresses)



@task(name='send-email')
def send_published_article(date_string, sender, recipient, subject, byline, email_text, story_text, attachment=None):
    """
    Task for sending each email, gets called by create_email_batch
    """    
    email = EMail(subject, recipient)
    ctx = {'subject': subject, 'story_text': story_text, 'email_text': email_text, 'byline': byline}
    email.text('../templates/templated_email/emaila.txt', ctx)
    email.html('../templates/templated_email/emaila.html', ctx)  
    if attachment:
        email.add_attachment(attachment)
    email.send()


@task(name='email_report')
def email_report(sender, recipients, report_subject, story_title, email_addresses):
    """
    Task for sending email report to editors with list of email addresses to which stories are sent
    """    
    for r in recipients:
        email = EMail(report_subject, r)
        ctx = {'report_subject': report_subject, 'story_title': story_title, 'email_addresses': email_addresses}
        email.text('../templates/templated_email/emailreport.txt', ctx)
        email.html('../templates/templated_email/emailreport.html', ctx)  
        email.send()


@task()
def report_errors():
        logging.error("reporting errors")