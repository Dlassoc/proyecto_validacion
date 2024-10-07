from django.test import TestCase, Client
from django.urls import reverse
from flight.models import User 

class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    #Usuario correcto y contraseña correcta
    def test_login_success(self):
        
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)  
        self.assertRedirects(response, reverse('index'))
    
    #Usuario incorrecto y contraseña correcta
    def test_login_failure_wrong_user(self):
        response = self.client.post(reverse('login'), {
            'username': 'wrongtestuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)  
        self.assertContains(response, "Invalid username and/or password.")

    #Usuario correcto y contraseña incorrecta
    def test_login_failure_wrong_password(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  
        self.assertContains(response, "Invalid username and/or password.")

    #Usuario incorrecto y contraseña incorrecta
    def test_login_failure_wrong(self):
        response = self.client.post(reverse('login'), {
            'username': 'wrongtestuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  
        self.assertContains(response, "Invalid username and/or password.")
    
    #Usuario vacio y contraseña vacia
    def test_login_failure_empty(self):
        response = self.client.post(reverse('login'), {
            'username': '',
            'password': ''
        })
        self.assertEqual(response.status_code, 200)  
        self.assertContains(response, "Invalid username and/or password.")
        
    def test_login_redirect_if_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
    
    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flight/login.html')