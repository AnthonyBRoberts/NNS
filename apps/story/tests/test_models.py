from mock import Mock
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test.client import RequestFactory
from django.test import TestCase
from story.models import Article

class StoryModelTest(TestCase):
	fixtures = ['testdata.json']

	def setUp(self):
		# Every test needs access to the request factory.
		self.factory = RequestFactory()
		self.author = User.objects.get(username='jmoore')

	def test_can_create_story_with_slug(self):
		story = Article.objects.create(author=self.author, title='Article Model Unit Test Story')
		self.assertIn('article-model-unit-test-story', story.slug)

	def test_article_unicode(self):
		mock_article = Mock(spec=Article)
		mock_article.author=self.author
		mock_article.title='test unicode test'
		self.assertEqual(Article.__unicode__(mock_article), 'test unicode test')

	def test_article_get_absolute_url(self):
		story = Article.objects.create(author=self.author, title='Article Model Unit Test Story')
		self.assertIsNotNone(story.get_absolute_url())

	def test_can_edit_story(self):
		story = Article.objects.get(slug='test-new-story-12-feb-2014')
		story.text = 'Some new text for the story'
		story.title = 'Some new title for the story'
		story.save()
		self.assertIn('Some new text for the story', story.text)
		# make sure the slug doesn't change when you change the title.
		self.assertIn('test-new-story-12-feb-2014', story.slug)