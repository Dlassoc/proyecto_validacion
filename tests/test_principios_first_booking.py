from django.test import TestCase
from django.urls import reverse
from flight.models import Ticket, User


class BookingsViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.ticket1 = Ticket.objects.create(
            user=self.user,
            ref_no='ABC123',
            flight_ddate='2024-10-20',
            status='confirmed'
        )
        self.ticket2 = Ticket.objects.create(
            user=self.user,
            ref_no='XYZ456',
            flight_ddate='2024-10-21',
            status='confirmed'
        )

    def test_bookings_view_authenticated(self):
        self.client.login(username='testuser', password='testpass')

        response = self.client.get(reverse('bookings'))

        self.assertEqual(response.status_code, 200)

        self.assertIn('tickets', response.context)
        self.assertEqual(len(response.context['tickets']), 2)
        self.assertContains(response, 'ABC124')
        self.assertContains(response, 'XYZ457')

    def test_bookings_view_not_authenticated(self):
        response = self.client.get(reverse('bookings'))
        self.assertRedirects(response, reverse('login'))
