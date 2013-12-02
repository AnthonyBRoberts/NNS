from celery import task
from story.email import EMail, log_email
import logging
import datetime
import time


@task(name='email-batch')
def create_email_batch(date_string, sender, recipients, subject, byline, email_text, story_text, attachment=None):
    """
    Task for emailing published articles.
    Runs when an article is saved and both is_published & send_now==True
    """  
    for r in recipients:
        send_published_article.delay(date_string, sender, r, subject,
                                                        byline, email_text, story_text, attachment)
        time.sleep(2)


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
    #log_email(recipient, date_string)

@task()
def report_errors():
        logging.error("reporting errors")