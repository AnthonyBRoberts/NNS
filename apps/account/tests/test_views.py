from django.core.urlresolvers import resolve, reverse
from django.contrib.auth.models import User
from django.test.utils import IgnoreDeprecationWarningsMixin
from django.test.client import RequestFactory
from django.shortcuts import get_object_or_404
from django.test import TestCase
from profiles.views import edit_profile
from account.views import client_index, reporter_index, editor_index
from account.forms import UnsubscribeForm
from account.tasks import *

class AccountViewsTests(TestCase):
	fixtures = ['../../functional_tests/fixtures/testdata.json']

	def setUp(self):
		# Every test needs access to the request factory.
		self.factory = RequestFactory()
		self.user = User.objects.get(username='jmoore')
		self.client = User.objects.get(email='anthony@lincolnultimate.com')

	def test_client_list_view(self):
		request = self.factory.get(reverse('profiles_profile_list'))
		request.user = self.user
		response = client_index(request)
		self.assertEqual(response.status_code, 200)

	def test_reporter_list_view(self):
		request = self.factory.get(reverse('profiles_reporter_list'))
		request.user = self.user
		response = reporter_index(request)
		self.assertEqual(response.status_code, 200)

	def test_editor_list_view(self):
		request = self.factory.get(reverse('profiles_editor_list'))
		request.user = self.user
		response = editor_index(request)
		self.assertEqual(response.status_code, 200)

	def test_unsubscribe_view(self):
		request = self.factory.get(reverse('unsubscribe'))
		request.user = self.client
		response = edit_profile(request, UnsubscribeForm)
		self.assertEqual(response.status_code, 200)

	def test_unsubscribe_view_post(self):
		request = self.factory.get(reverse('unsubscribe'))
		request.user = self.client
		response = edit_profile(request, UnsubscribeForm)
		self.assertTemplateUsed('profiles/unsubscribe.html')