from django.test import TestCase
from users.models import User
from blogs.models import Post, Edition, Quote, Tag


class PostTests(TestCase):

    def setUp(self):
        self.new_user = User.objects.create(username='blah', password='blah')

    def test_can_create_with_edition(self):
        new_post = Post.objects.create_with_edition(title='test', author=self.new_user, text='This is the post')

        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Edition.objects.count(), 1)

        test_post = Post.objects.first()
        test_edition = Edition.objects.first()

        self.assertEqual(test_post.title, 'test')
        self.assertEqual(test_post.author, new_user)

        self.assertEqual(test_edition.post, new_post)
        self.assertEqual(test_edition.text, 'test')

    def test_can_get_reference_if_post(self):
        new_post = Post.objects.create_with_edition(title='test', author=self.new_user, text='Test is a test.')

        new_post_reply = Post.objects.create_with_edition(title='test', author=self.new_user, text='Test is a test.')
        new_post_reply.set_reference(new_post)
        new_post_reply.save()

        self.assertEqual(Post.objects.count(), 2)
