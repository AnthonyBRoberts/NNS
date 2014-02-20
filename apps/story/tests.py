from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from story.views import FrontpageView


class StoryViewsTestCase(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
