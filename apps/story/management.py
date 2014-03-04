import time
from django.conf import settings
from django.db.models import signals
from django.db.models import Q
from django.utils.translation import ugettext_noop as _
from story.tasks import create_email_batch, email_editor
from apps.account.models import UserProfile
from notification import models as notification


def create_notice_types(app, created_models, verbosity, **kwargs):
	notification.create_notice_type("reporter_story_update", _("Reporter Story Update"), _("A reporter has updated a story"))
	notification.create_notice_type("editor_story_update", _("Editor Story Update"), _("An editor has updated your story"))

signals.post_syncdb.connect(create_notice_types, sender=notification)


def notify_editor(article):
	subject = article.title + ' is ready for an editor'
	byline = article.author.get_profile().byline
	story_text = article.text 
	email_editor.delay(article.author.email, subject, byline, story_text)


def send_article(article, form):
	subject = article.title
	byline = article.byline
	email_text = article.email_text
	story_text = article.text
	author_email = article.author.email
	media = article.mediaitems.all()
	mediaitems = []
	for m in media:
		mediaitems.append(m.docfile.url)
	bc_only = form.cleaned_data['broadcast_only']
	add_email_only = form.cleaned_data['add_recipients_only']
	add_email_list = form.cleaned_data['add_recipients']
	recipients = []
	date_string = time.strftime("%Y-%m-%d-%H-%M")
	if add_email_only:
		for r in add_email_list:
			recipients.append(r)
	else: 
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
		if add_email_list:
			for r in add_email_list:
				recipients.append(r)
	if article.docfile is not None:
		attachment = article.docfile
		create_email_batch.delay(date_string, author_email, recipients, subject,
										byline, email_text, story_text, attachment, mediaitems)
	else:
		create_email_batch.delay(date_string, author_email, recipients, subject,
										byline, email_text, story_text, mediaitems)