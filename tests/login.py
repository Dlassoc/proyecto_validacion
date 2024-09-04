from django.test import TestCase, Client
from django.urls import reverse
from flight.models import User  # Importa el modelo de usuario personalizado

class LoginViewTestCase(TestCase):

    def setUp(self):
        # Configura un cliente de prueba
        self.client = Client()
        # Crea un usuario de prueba utilizando el modelo personalizado
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    #Usuario correcto y contraseña correcta
    def test_login_success(self):
        # Prueba un inicio de sesión exitoso
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)  # Redirige a la página principal
        self.assertRedirects(response, reverse('index'))
    
    #Usuario incorrecto y contraseña correcta
    def test_login_failure(self):
        # Prueba un inicio de sesión fallido
        response = self.client.post(reverse('login'), {
            'username': 'wrongtestuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)  # Permanece en la página de inicio de sesión
        self.assertContains(response, "Invalid username and/or password.")

    #Usuario correcto y contraseña incorrecta
    def test_login_failure(self):
        # Prueba un inicio de sesión fallido
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Permanece en la página de inicio de sesión
        self.assertContains(response, "Invalid username and/or password.")

    #Usuario incorrecto y contraseña incorrecta
    def test_login_failure(self):
        # Prueba un inicio de sesión fallido
        response = self.client.post(reverse('login'), {
            'username': 'wrongtestuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Permanece en la página de inicio de sesión
        self.assertContains(response, "Invalid username and/or password.")
    
    #Usuario vacio y contraseña vacia
    def test_login_failure(self):
        # Prueba un inicio de sesión fallido
        response = self.client.post(reverse('login'), {
            'username': '',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Permanece en la página de inicio de sesión
        self.assertContains(response, "Invalid username and/or password.")
    
    def test_login_view_get(self):
        # Prueba el acceso a la vista de login mediante GET
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flight/login.html')