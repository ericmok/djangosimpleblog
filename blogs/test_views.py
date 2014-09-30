from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

from blogs.models import Post, Edition


User = get_user_model()


class PostViews(TestCase):

    def setUp(self):
        self.client = Client()

    def test_GET_post_create(self):
        new_user = get_user_model().objects.create_user(username='asdf', password='asdf')
        self.client.login(username='asdf', password='asdf')
        response = self.client.get(reverse('posts-create'))
        self.assertEqual(response.status_code, 200)

    def test_GET_post_create_401(self):
        response = self.client.get(reverse('posts-create'))
        self.assertEqual(response.status_code, 302)

    def test_POST_post_create(self):
        new_user = get_user_model().objects.create_user(username='asdf', password='asdf')
        self.client.login(username='asdf', password='asdf')
        response = self.client.post(reverse('posts-create'), data={
                'title': 'Test',
                'text': 'Some text'
            })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 1)

    def test_GET_post_detail(self):
        user = User.objects.create_user(username='asdf', password='asdf')
        new_post = Post.objects.create_with_edition(title='test', author=user, text='This is a test.')
        
        response = self.client.get(reverse('posts-detail', kwargs={'slug': 'test'}))
        self.assertEqual(response.status_code, 200)
        
        # Test slug
        new_post = Post.objects.create_with_edition(title='test', author=user, text='This is a test.')
        
        response = self.client.get(reverse('posts-detail', kwargs={'slug': '0test'}))
        self.assertEqual(response.status_code, 200)        

    def test_GET_post_detail_on_not_found(self):
        user = User.objects.create_user(username='asdf', password='asdf')
        new_post = Post.objects.create_with_edition(title='test', author=user, text='This is a test.')
        
        response = self.client.get(reverse('posts-detail', kwargs={'slug': 'testasdf'}))
        self.assertEqual(response.status_code, 404)

    def test_GET_post_list(self):
        user = User.objects.create_user(username='asdf', password='asdf')
        new_post = Post.objects.create_with_edition(title='another test', author=user, text='This is a test.')
        
        response = self.client.get(reverse('posts-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'another test')

    def test_GET_post_update(self):
        user = User.objects.create_user(username='asdf', password='asdf')
        new_post = Post.objects.create_with_edition(title='Another', author=user, text='This is a test.')

        self.client.login(username='asdf', password='asdf')
        response = self.client.get(reverse('posts-update', kwargs={'slug': new_post.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context.get('form', None))
        self.assertIsNotNone(response.context.get('post', None))

    def test_GET_post_update_401(self):
        user = User.objects.create_user(username='asdf', password='asdf')
        new_post = Post.objects.create_with_edition(title='Another', author=user, text='This is a test.')

        response = self.client.get(reverse('posts-update', kwargs={'slug': new_post.slug}))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('posts-update', kwargs={'slug': new_post.slug}), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_POST_post_update_view(self):
        user = User.objects.create_user(username='asdf', password='asdf')
        new_post = Post.objects.create_with_edition(title='Another', author=user, text='This is a test.')

        self.client.login(username='asdf', password='asdf')
        data = {'text': 'Changed'}
        response = self.client.post(reverse('posts-update', kwargs={'slug': new_post.slug}), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(new_post.editions.first().text, 'Changed')
