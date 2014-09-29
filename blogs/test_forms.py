from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model

from blogs.models import Post, Edition
from blogs.forms import PostModelForm, PostCreationForm


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