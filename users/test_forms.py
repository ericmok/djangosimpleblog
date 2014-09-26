from django.test import TestCase
from django.core.urlresolvers import reverse

from users.forms import RegisterForm
from users.models import User


class RegisterFormTest(TestCase):

    def test_can_save(self):
        self.assertEqual(User.objects.count(), 0)

        test_form = RegisterForm({'username': 'blah', 
                                  'email': 'tim@google.com', 
                                  'password1': 'asdf',
                                  'password2': 'asdf'})
        test_form.is_valid()
        test_form.save()

        self.assertEqual(User.objects.count(), 1)

    def test_not_valid_with_non_matching_passwords(self):
        self.assertEqual(User.objects.count(), 0)

        test_form = RegisterForm({'username': 'blah', 
                                  'email': 'tim@google.com', 
                                  'password1': 'asdf',
                                  'password2': 'asdf2'})
        test_form.is_valid()

        def test_this():
            test_form.save()

        self.assertRaises(ValueError, test_this)

        self.assertEqual(User.objects.count(), 0)