from celery import task
from story.email import EMail
from apps.account.models import UserProfile
from async_messages import message_users
from django.contrib.messages import constants
import logging
import time
import datetime



@task(name='email-batch')
def create_email_batch(date_string, sender, recipients, subject, byline, email_text, story_text, mediaitems=None, attachment=None):
    """
    Task for emailing published articles.
    Calls a subtask for each recipient, so it sends one email at a time.
    2 second sleep to avoid AWS rate limits
    Task is called by story management command send_article
    message_users is an async_messages object and notification is sent to all Editors
    """
    
    for r in recipients:
        send_published_article.delay(date_string, sender, r, subject,
                                                        byline, email_text, story_text, attachment, mediaitems)
        time.sleep(2)
    msg = "Emails for story: \"" + subject + "\" -- " + byline + " has been sent on " + datetime.datetime.now().strftime("%m/%d/%Y - at %I:%M %p")
    recip = UserProfile.objects.filter(user_type = 'Editor')
    message_users(recip, msg, constants.SUCCESS)


@task(name='send-email')
def send_published_article(date_string, sender, recipient, subject, byline, email_text, story_text, mediaitems=None, attachment=None):
    """
    Task for sending each email, gets called by create_email_batch
    """
    email = EMail(subject, recipient)
    ctx = {'subject': subject, 'story_text': story_text, 'email_text': email_text, 'byline': byline, 'mediaitems': mediaitems}
    email.text('../templates/templated_email/emaila.txt', ctx)
    email.html('../templates/templated_email/emaila.html', ctx)
    if attachment:
        email.add_attachment(attachment)
    email.send()

@task(name='email_editor')
def email_editor(sender, subject, byline, text):
    """
    Task for sending email on stories marked as ready_for_editor in a submitted reporter form.
    """
    recipients = []
    for profile in UserProfile.objects.filter(user_type = 'Editor'):
                            recipients.append(profile.user.email)    
    for r in recipients:
        email = EMail(subject, r)
        ctx = {'subject': subject, 'byline': byline, 'text': text}
        email.text('../templates/templated_email/ready_for_editor.txt', ctx)
        email.html('../templates/templated_email/ready_for_editor.html', ctx)  
        email.send()
