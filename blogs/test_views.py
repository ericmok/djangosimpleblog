from django.test import TestCase, Client
from django.core.urlresolvers import reverse

class PostViews(TestCase):

    def setUp(self):
        self.client = Client()

    def test_post_create(self):
        response = self.client.get(reverse('post-create'))
        self.assertEqual(response.status_code, 200)