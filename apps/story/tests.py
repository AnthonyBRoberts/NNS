from django.test import TestCase


class StoryViewsTestCase(TestCase):
    def test_index(self):
        """
        Tests Story Index (recent stories).
        """
        resp = self.client.get('/story/')
        self.assertEqual(resp.status_code, 200)

