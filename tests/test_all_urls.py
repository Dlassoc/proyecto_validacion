# tests/test_urls.py

from django.test import SimpleTestCase
from django.urls import reverse
from mockito import mock, when, verify
from flight.views import index, login_view, logout_view, register_view


class UrlsTests(SimpleTestCase):

    def setUp(self):
        self.index_view = mock(index)
        self.login_view = mock(login_view)
        self.logout_view = mock(logout_view)
        self.register_view = mock(register_view)

    def test_index_url(self):
        when(self.index_view).request = None
        response = self.client.get(reverse('index'))
        verify(self.index_view).request
        self.assertEqual(response.status_code, 200)

    def test_login_url(self):
        when(self.login_view).request = None
        response = self.client.get(reverse('login'))
        verify(self.login_view).request
        self.assertEqual(response.status_code, 200)

    def test_logout_url(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

    def test_register_url(self):
        when(self.register_view).request = None
        response = self.client.get(reverse('register'))
        verify(self.register_view).request
        self.assertEqual(response.status_code, 200)
