from django.conf import settings
from django.test.utils import override_settings
from django.test import TestCase
from account.models import UserProfile
from account.tasks import new_client_alert

class AccountTasksTests(TestCase):
	fixtures = ['../../functional_tests/fixtures/testdata.json']

	@override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
					   CELERY_ALWAYS_EAGER=True,
					   BROKER_BACKEND='memory')
	def test_new_client_alert_task(self):
		subject = 'New Client Signup'
		text = 'client_email@gmail.com'
		sender = settings.DEFAULT_FROM_EMAIL
		recipients = []
		for profile in UserProfile.objects.filter(user_type = 'Editor'):
			recipients.append(profile.user.email)
		result = new_client_alert.delay(recipients, text)
		self.assertTrue(result.successful())
