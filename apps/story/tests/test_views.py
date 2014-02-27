from django.core.urlresolvers import resolve, reverse
from django.contrib.auth.models import User
from django.test.utils import IgnoreDeprecationWarningsMixin
from django.test.client import RequestFactory
from django.shortcuts import get_object_or_404
from django.test import TestCase
from story.views import *

class StoryViewsTests(TestCase):
	fixtures = ['../../functional_tests/fixtures/testdata.json']

	def setUp(self):
		# Every test needs access to the request factory.
		self.factory = RequestFactory()
		self.user = User.objects.get(username='jmoore')

	def create_story_content(self):
		story = Article()
		story.author = self.user
		story.title = "Unit Test Story Title"
		story.text = "Unit Test Story Text"
		story.save()
		return self.factory.post(
			reverse('story_article_add'),
			data={'author': story.author, 'title': story.title, 'text': story.text}
		)

	def test_root_url_shows_home_page_content(self):
		response = self.client.get(reverse('index'))
		self.assertTemplateUsed(response, 'welcome_content.html')
		self.assertEqual(response.status_code, 200)

	def test_about_url_shows_aboutus_content(self):
		response = self.client.get(reverse('about'))
		self.assertTemplateUsed(response, 'about.html')
		self.assertEqual(response.status_code, 200)

	def test_reporter_docs_content(self):
		response = self.client.get(reverse('reporterdocs'))
		self.assertTemplateUsed(response, 'reporterdocs.html')
		self.assertEqual(response.status_code, 200)

	def test_story_list_view(self):
		request = self.factory.get(reverse('story_article_index'))
		request.user = self.user
		response = story_index(request)
		self.assertEqual(response.status_code, 200)

	def test_story_inprogress_list_view(self):
		request = self.factory.get(reverse('inprogress_list'))
		request.user = self.user
		response = inprogress_index(request)
		self.assertEqual(response.status_code, 200)

	def test_add_story_view(self):
		request = self.factory.get(reverse('story_article_add'))
		request.user = self.user
		response = add_article(request)
		self.assertEqual(response.status_code, 200)

	def test_create_story_renders_story_form_template(self):
		response = self.create_story_content()
		self.assertTemplateUsed(response, 'article_form.html')

	def test_edit_story_view(self):
		request = self.factory.get(reverse('story_article_edit', kwargs={'slug': 'front-page'}))
		request.user = self.user
		response = edit_article(request, slug='front-page')
		self.assertEqual(response.status_code, 200)
