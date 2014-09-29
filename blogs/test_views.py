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

    def test_post_create_post_request(self):
        get_user_model().objects.create_user(username='asdf', password='asdf')
        self.client.login(username='asdf', password='asdf')
        response = self.client.post(reverse('posts-create'), data={
                'title': 'Test'
            })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 1)

    def test_post_detail_get_request(self):
        user = User.objects.create_user(username='asdf', password='asdf')
        new_post = Post.objects.create_with_edition(title='test', author=user, text='This is a test.')
        
        response = self.client.get(reverse('posts-detail', kwargs={'slug': 'test'}))
        self.assertEqual(response.status_code, 200)
        
        # Test slug
        new_post = Post.objects.create_with_edition(title='test', author=user, text='This is a test.')
        
        response = self.client.get(reverse('posts-detail', kwargs={'slug': '0test'}))
        self.assertEqual(response.status_code, 200)        

    def test_post_detail_get_request_on_not_found(self):
        user = User.objects.create_user(username='asdf', password='asdf')
        new_post = Post.objects.create_with_edition(title='test', author=user, text='This is a test.')
        
        response = self.client.get(reverse('posts-detail', kwargs={'slug': 'testasdf'}))
        self.assertEqual(response.status_code, 404)