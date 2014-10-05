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

    def test_GET_post_detail_has_context_data(self):
        user = User.objects.create_user(username='asdf', password='asdf')
        new_post = Post.objects.create_with_edition(title='test', author=user, text='This is a test.')
        
        response = self.client.get(reverse('posts-detail', kwargs={'slug': 'test'}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('posts' in response.context)

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
        self.assertTrue('form' in response.context)
        self.assertTrue('post' in response.context)

    def test_GET_post_update_with_no_login(self):
        """
        Unauthorized 
        """
        user = User.objects.create_user(username='asdf', password='asdf')
        new_post = Post.objects.create_with_edition(title='Another', author=user, text='This is a test.')

        response = self.client.get(reverse('posts-update', kwargs={'slug': new_post.slug}))
        # 401 is tricky
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('posts-update', kwargs={'slug': new_post.slug}), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_GET_post_update_raise_403_if_wrong_user(self):
        user = User.objects.create_user(username='asdf', password='asdf')
        bad_user = User.objects.create_user(username='bunny', password='asdf')

        new_post = Post.objects.create_with_edition(title='Another', author=user, text='This is a test.')

        self.client.login(username='bunny', password='asdf')
        data = {'text': 'Changed'}
        response = self.client.post(reverse('posts-update', kwargs={'slug': new_post.slug}), data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(new_post.editions.first().text, 'This is a test.')

    def test_POST_post_update_view(self):
        user = User.objects.create_user(username='asdf', password='asdf')
        new_post = Post.objects.create_with_edition(title='Another', author=user, text='This is a test.')

        self.client.login(username='asdf', password='asdf')
        data = {'text': 'Changed'}
        response = self.client.post(reverse('posts-update', kwargs={'slug': new_post.slug}), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(new_post.editions.first().text, 'Changed')

    def test_GET_delete_post_view(self):
        user = User.objects.create_user(username='asdf', password='asdf')
        new_post = Post.objects.create_with_edition(title='Another', author=user, text='This is a test.')

        self.client.login(username='asdf', password='asdf')
        response = self.client.get(reverse('posts-delete', kwargs={'slug': new_post.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.count(), 1)

    def test_POST_delete_post_view(self):
        user = User.objects.create_user(username='asdf', password='asdf')
        new_post = Post.objects.create_with_edition(title='Another', author=user, text='This is a test.')
        new_edition = Edition.objects.create(post=new_post, text='blah')
        
        self.client.login(username='asdf', password='asdf')
        response = self.client.post(reverse('posts-delete', kwargs={'slug': new_post.slug}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 0)
        self.assertEqual(Edition.objects.count(), 0)

    def test_delete_post_no_slug(self):
        user = User.objects.create_user(username='asdf', password='asdf')
        new_post = Post.objects.create_with_edition(title='Another', author=user, text='This is a test.')

        response = self.client.get(reverse('posts-delete', kwargs={'slug': ''}))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Post.objects.count(), 1)

    def test_delete_post_no_credentials(self):
        user = User.objects.create_user(username='asdf', password='asdf')
        new_post = Post.objects.create_with_edition(title='Another', author=user, text='This is a test.')

        # GET
        response = self.client.get(reverse('posts-delete', kwargs={'slug': new_post.slug}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 1)

        # POST
        response = self.client.post(reverse('posts-delete', kwargs={'slug': new_post.slug}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 1)