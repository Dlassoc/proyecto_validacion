from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from flight.models import Ticket
from django.http import JsonResponse


class CancelTicketViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser', password='testpass')
        self.ticket = Ticket.objects.create(
            ref_no='ABC123', user=self.user, status='BOOKED')

    def test_cancel_ticket_success(self):
        # Arrange
        self.client.login(username='testuser', password='testpass')
        data = {'ref': 'ABC123'}

        # Act
        response = self.client.post(reverse('cancelticket'), data)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True})
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, 'CANCELLED')

    def test_cancel_ticket_user_unauthorized(self):
        # Arrange
        another_user = get_user_model().objects.create_user(
            username='anotheruser', password='anotherpass')
        self.client.login(username='anotheruser', password='anotherpass')
        data = {'ref': 'ABC123'}

        # Act
        response = self.client.post(reverse('cancelticket'), data)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
                             'success': False, 'error': "User unauthorised"})
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, 'BOOKED')

    def test_cancel_ticket_not_authenticated(self):
        # Arrange
        data = {'ref': 'ABC123'}

        # Act
        response = self.client.post(reverse('cancelticket'), data)
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "User unauthorised")
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, 'BOOKED')

    def test_cancel_ticket_method_not_post(self):
        # Act
        response = self.client.get(reverse('cancelticket'))

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "Method must be POST.")
