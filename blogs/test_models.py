from django.test import TestCase
from django.db import IntegrityError

from users.models import User
from blogs.models import Post, Edition, Tag


class PostTests(TestCase):

    def setUp(self):
        self.new_user = User.objects.create(username='Alice', password='passwordasdf')

    def test_can_create_with_edition(self):
        new_post = Post.objects.create_with_edition(title='test', author=self.new_user, text='This is the post')

        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Edition.objects.count(), 1)

        test_post = Post.objects.first()
        test_edition = Edition.objects.first()

        self.assertEqual(test_post.title, 'test')
        self.assertEqual(test_post.author, self.new_user)

        self.assertEqual(test_edition.post, new_post)
        self.assertEqual(test_edition.text, 'This is the post')

    def test_can_generate_unique_slug(self):
        test_title = 'Test title'
        post = Post(title=test_title, author=self.new_user)
        post.generate_unique_slug()
        post.save()
        self.assertEqual(post.slug, 'test-title')

        post = Post(title=test_title, author=self.new_user)
        post.generate_unique_slug()
        post.save()
        self.assertEqual(post.slug, '0test-title')

        post = Post(title=test_title, author=self.new_user)
        post.generate_unique_slug()
        post.save()
        self.assertEqual(post.slug, '1test-title')