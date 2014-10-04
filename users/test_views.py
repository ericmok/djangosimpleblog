from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import SESSION_KEY

from django.utils.six.moves.urllib.parse import urlparse

from users.models import User


class RegisterTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_register_view(self):
        response = self.client.get(reverse('users-register'))
        self.assertEqual(response.status_code, 200)

    def test_can_register_user(self):
        self.assertEqual(User.objects.count(), 0)
        response = self.client.post(reverse('users-register'), 
                                    data={'username':'blah', 
                                          'password1':'blah',
                                          'password2':'blah'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 1)

    def test_redirects_on_success(self):
        self.assertEqual(User.objects.count(), 0)
        response = self.client.post(reverse('users-register'), 
                                    data={'username':'blah', 
                                          'password1':'blah',
                                          'password2':'blah'}, follow=True)
        self.assertEqual(response.status_code, 200)
        scheme, netloc, path, params, query, fragment = urlparse(response.redirect_chain[0][0])
        self.assertEqual(path, '/')
        self.assertEqual(User.objects.count(), 1)


class SignInCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_can_login(self):
        user = User.objects.create_user(username='blah', password='blah')
        response = self.client.post(reverse('users-signin'), data={'username': user.username, 'password': 'blah'})
        self.assertEqual(response.status_code, 302)

    def test_can_logout(self):
        response = self.client.get(reverse('users-signout'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(SESSION_KEY not in self.client.session)