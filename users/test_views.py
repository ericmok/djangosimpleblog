from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from users.models import User


class RegisterTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_register_view(self):
        response = self.client.get(reverse('users-register'))
        self.assertEqual(response.status_code, 200)

class LoginTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_can_login(self):
        user = User.objects.create(username='blah', password='blah')
        response = self.client.post(reverse('users-login'), data={'username': user.username, 'password': user.password})
        self.assertEqual(response.status_code, 301)