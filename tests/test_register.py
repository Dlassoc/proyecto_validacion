from django.test import TransactionTestCase, Client
from django.urls import reverse
from flight.models import User

class RegisterViewTestCase(TransactionTestCase):

    def setUp(self):
        self.client = Client()

    def test_register_success(self):
        response = self.client.post(reverse('register'), {
            'firstname': 'John',
            'lastname': 'Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password': 'password123',
            'confirmation': 'password123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='johndoe').exists())
        self.assertRedirects(response, reverse('index'))

    def test_register_password_mismatch(self):
        response = self.client.post(reverse('register'), {
            'firstname': 'Jane',
            'lastname': 'Doe',
            'username': 'janedoe',
            'email': 'janedoe@example.com',
            'password': 'password123',
            'confirmation': 'password456'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Passwords must match.")
        self.assertFalse(User.objects.filter(username='janedoe').exists())

    def test_register_special_character(self):
        response = self.client.post(reverse('register'), {
            'firstname': 'Joh4n!',
            'lastname': 'Doe#',
            'username': 'joseluis',
            'email': 'joseluis@example.com',
            'password': 'password123',
            'confirmation': 'password123'
        })
        self.assertEqual(response.status_code, 200)  
        self.assertContains(response, "Invalid characters in name or lastname.")  
        self.assertFalse(User.objects.filter(username='joseluis').exists())  


    def test_register_username_taken(self):
        User.objects.create_user(username='johndoe', email='johndoe@example.com', password='password123')
        
        response = self.client.post(reverse('register'), {
            'firstname': 'John',
            'lastname': 'Doe',
            'username': 'johndoe',
            'email': 'johnny@example.com',
            'password': 'newpassword123',
            'confirmation': 'newpassword123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Username already taken.")
        self.assertEqual(User.objects.filter(username='johndoe').count(), 1)

    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flight/register.html')
