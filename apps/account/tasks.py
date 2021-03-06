from celery import task
from story.email import EMail

@task(name='new_client_alert')
def new_client_alert(recipients, text):
    """
    Task for sending email on new client sign-up
    """
    subject = 'New Client Signup'
    for r in recipients:
        email = EMail(subject, r)
        ctx = {'subject': subject, 'text': text}
        email.text('../templates/templated_email/newclientalert.txt', ctx)
        email.html('../templates/templated_email/newclientalert.html', ctx)  
        email.send()
