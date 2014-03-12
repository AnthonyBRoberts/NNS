import time
from django.contrib.auth.models import User
from django.test.utils import override_settings
from django.test.client import RequestFactory
from django.test import TestCase
from account.models import UserProfile
from story.models import Article
from story.tasks import *

class StoryTasksTests(TestCase):
	fixtures = ['../../functional_tests/fixtures/testdata.json']

	@override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
                       CELERY_ALWAYS_EAGER=True,
                       BROKER_BACKEND='memory')
	def test_create_email_batch_send_to_all_clients_task(self):
		story = Article.objects.get(slug='about-us')
		date_string = time.strftime("%Y-%m-%d-%H-%M")
		sender = story.author.email
		recipients = []
		for profile in UserProfile.objects.filter(user_type = 'Editor'):
			recipients.append(profile.user.email)
		for profile in UserProfile.objects.filter(user_type = 'Reporter'):        
			recipients.append(profile.user.email)
		for profile in UserProfile.objects.filter(user_type = 'Client'):        
			recipients.append(profile.user.email)
		subject = story.title
		byline = story.byline
		email_text = story.email_text
		story_text = story.text
		result = create_email_batch.delay(date_string, sender, recipients, subject, byline, email_text, story_text)
		self.assertTrue(result.successful())

	@override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
                       CELERY_ALWAYS_EAGER=True,
                       BROKER_BACKEND='memory')
	def test_send_published_article_task(self):
		story = Article.objects.get(slug='about-us')
		date_string = time.strftime("%Y-%m-%d-%H-%M")
		sender = story.author.email
		recipient = 'nns.aroberts@gmail.com'
		subject = story.title
		byline = story.byline
		email_text = story.email_text
		story_text = story.text
		result = send_published_article.delay(date_string, sender, recipient, subject, byline, email_text, story_text)
		self.assertTrue(result.successful())

	@override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
                       CELERY_ALWAYS_EAGER=True,
                       BROKER_BACKEND='memory')
	def test_email_editor_task(self):
		story = Article.objects.get(slug='about-us')
		sender = story.author.email
		subject = story.title
		byline = story.byline
		text = story.text
		result = email_editor.delay(sender, subject, byline, text)
		self.assertTrue(result.successful())