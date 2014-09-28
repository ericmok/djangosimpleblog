from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


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
        response = self.client.post(reverse('users-login'))
        self.assertEqual(response.status_code, 301)