from django.test import TestCase
from django.db import IntegrityError

from users.models import User
from blogs.models import Post, Edition, Quote, Tag


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

    def test_can_set_reference_from_model_with_edition(self):
        new_post = Post.objects.create_with_edition(title='test', author=self.new_user, text='Test is a test.')

        new_post_reply = Post.objects.create_with_edition(title='test', author=self.new_user, text='Test is a test.')
        new_post_reply.set_reference_from_model(new_post.editions.first())
        new_post_reply.save()

        self.assertEqual(Post.objects.count(), 2)

    def test_can_set_reference_from_model_with_quote(self):
        new_post = Post.objects.create_with_edition(title='test', author=self.new_user, text='Test is a test.')

        new_post_reply = Post.objects.create_with_edition(title='test', author=self.new_user, text='Test is a test.')
        new_post_reply.set_reference_from_model(new_post.editions.first())
        new_post_reply.save()

        self.assertEqual(Post.objects.count(), 2)

    def test_raise_error_when_set_reference_from_model_with_wrong_model(self):
        new_post = Post.objects.create_with_edition(title='test', author=self.new_user, text='Test is a test.')
        def should_throw_error():
            new_post.set_reference_from_model(User.objects.create(username='blah', password='blah'))

        self.assertRaises(ValueError, should_throw_error)


    def test_can_set_reference_from_type_and_id(self):
        new_post = Post.objects.create_with_edition(title='test', author=self.new_user, text='Test is a test.')

        new_post_reply = Post.objects.create_with_edition(title='test', author=self.new_user, text='Test is a test.')
        new_post_reply.set_reference_from_type_and_id('Edition', new_post.id)
        new_post_reply.save()

        self.assertEqual(Post.objects.count(), 2)
