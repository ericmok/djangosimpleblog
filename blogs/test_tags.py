from django.test import TestCase
from django.contrib.auth import get_user_model

from templatetags.present import present
from blogs.models import Post, Edition


class PresentTest(TestCase):
    def test_can_get_markdown(self):
        new_post = Post.objects.create_with_edition(title='test', author=self.new_user, text='#This is the post')
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Edition.objects.count(), 1)

        markdown_test = Post.objects.get(id=new_post.id).editions.first().text
        markdown_test = present(markdown_test)
        self.assertIn('<h1>', markdown_test)

    def test_markdown_takes_h1_and_img(self):
        new_post = Post.objects.create_with_edition(title='test', author=self.new_user, text='#This is the post\n\n\nThis is a test\n\n\nAnother [here](cat.png)')
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Edition.objects.count(), 1)

        markdown_test = Post.objects.get(id=new_post.id).editions.first().text
        markdown_test = present(markdown_test)
        self.assertIn('<h1>', markdown_test)
        self.assertIn('src=\"cat.png\"', markdown_test)

    def test_markdown_is_safe(self):
        new_post = Post.objects.create_with_edition(title='test', author=self.new_user, text='<script></script>')
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Edition.objects.count(), 1)

        markdown_test = Post.objects.get(id=new_post.id).editions.first().text
        markdown_test = present(markdown_test)
        self.assertNotIn('<script>', markdown_test)
        self.assertIn('&lt;script', markdown_test)