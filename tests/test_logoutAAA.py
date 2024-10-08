from django.test import TestCase
from django.urls import reverse
from flight.models import User
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect


class LogoutViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser', password='testpass')

    def test_logout_view_redirects_to_index(self):
        # Arrange
        self.client.login(username='testuser', password='testpass')

        # Act
        response = self.client.get(reverse('logout'))

        # Assert
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertRedirects(response, reverse('index'))
        self.assertNotIn('_auth_user_id', self.client.session)
