from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model

from blogs.models import Post, Edition
from blogs.forms import PostModelForm, PostCreationForm, PostUpdateForm


User = get_user_model()


class PostModelFormTest(TestCase):

    def test_save(self):
        self.assertEqual(User.objects.count(), 0)

        new_user = User.objects.create_user(username='blah', password='blah')

        new_post = Post(author=new_user)
        form = PostModelForm({'title': 'Cats'}, instance=new_post)
        result = form.is_valid()
        form.save()

        self.assertTrue(result)
        self.assertEqual(User.objects.count(), 1)


class PostCreationFormTest(TestCase):

    def test_save(self):
        self.assertEqual(User.objects.count(), 0)

        new_user = User.objects.create_user(username='blah', password='blah')

        request = RequestFactory().get('')
        request.user = new_user        

        form = PostCreationForm(request, {'title': 'Cats', 'text': 'Hi'})
        result = form.is_valid()
        form.save()

        self.assertTrue(result)
        self.assertEqual(User.objects.count(), 1)


class PostUpdateFormTest(TestCase):

    def test_constructor_instance_initialization(self):
        user_instance = get_user_model().objects.create_user(username='asdf', password='asdf')
        post_instance = Post.objects.create(title='Cats', author=user_instance)
        form = PostUpdateForm(data={'text': 'This is a test'}, instance=post_instance)
        self.assertTrue(form.is_valid())
        edition = form.save()

        self.assertEqual(Edition.objects.count(), 1)
        self.assertTrue(edition)

    def test_save(self):
        user_instance = get_user_model().objects.create_user(username='asdf', password='asdf')
        post_instance = Post.objects.create(title='Cats', author=user_instance)
        form = PostUpdateForm({'text': 'This is a test'})
        self.assertTrue(form.is_valid())
        edition = form.save(instance = post_instance)

        self.assertEqual(Edition.objects.count(), 1)
        self.assertTrue(edition)