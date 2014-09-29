from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

from blogs.models import Post, Edition


User = get_user_model()


class PostViews(TestCase):

    def setUp(self):
        self.client = Client()

    def test_post_create_get_request(self):
        response = self.client.get(reverse('posts-create'))
        self.assertEqual(response.status_code, 200)

    def test_post_detail_get_request(self):
        user = User.objects.create_user(username='asdf', password='asdf')
        new_post = Post.objects.create_with_edition(title='test', author=user, text='This is a test.')
        
        response = self.client.get(reverse('posts-detail', kwargs={'slug': 'test'}))
        self.assertEqual(response.status_code, 200)