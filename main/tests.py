from django.test import TestCase
from .models import User

class UserTest(TestCase):
    def setUp(self):
        User.objects.create(username='testuser', email='testuser@example.com')

    def test_username_content(self):
        user = User.objects.get(id=1)
        expected_object_name = f'{user.username}'
        self.assertEqual(expected_object_name, 'testuser')

    def test_email_content(self):
        user = User.objects.get(id=1)
        expected_object_email = f'{user.email}'
        self.assertEqual(expected_object_email, 'testuser@example.com')
