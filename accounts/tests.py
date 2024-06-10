from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')  # 'register' yerine gerçek URL adınızı kullanın

def test_register_GET(self): 
    response = self.client.get(self.register_url)

    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'registration/register.html')

def test_register_POST(self):
    response = self.client.post(self.register_url, {
        'username': 'fati',
        'password1': '12',
        'password2': 'test123',
        'first_name': 'Fatih',
        'last_name': 'User',
        'email': 'fatihr2@gmail.com',
        'role': 'Participant', 
    })

    self.assertEqual(response.status_code, 302)
    self.assertEqual(User.objects.last().email, 'testuser@example.com')