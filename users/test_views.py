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

    def test_can_register_user(self):
        self.assertEqual(User.objects.count(), 0)
        response = self.client.post(reverse('users-register'), data={'username':'blah', 'password':'blah'})
        self.assertEqual(response.status_code, 302)        
        self.assertEqual(User.objects.count(), 1)

class SignInCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_can_login(self):
        user = User.objects.create_user(username='blah', password='blah')
        response = self.client.post(reverse('users-signin'), data={'username': user.username, 'password': user.password})
        print('RESPONSE ' + response)
        self.assertEqual(response.status_code, 301)