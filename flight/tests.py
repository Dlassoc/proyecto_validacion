from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from flight.models import Ticket, Place, Flight, Week, Passenger
from datetime import timedelta, datetime
from django.http import HttpResponse

User = get_user_model()

class GetTicketTestCase(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Create a test place
        self.place_a = Place.objects.create(city='CityA', airport='AirportA', code='A1', country='CountryA')
        self.place_b = Place.objects.create(city='CityB', airport='AirportB', code='B1', country='CountryB')
        
        # Create a test week
        self.week = Week.objects.create(number=1, name='Monday')
        
        # Create a test flight
        self.flight = Flight.objects.create(
            origin=self.place_a,
            destination=self.place_b,
            depart_time='08:00:00',
            duration=timedelta(hours=2),  # Use timedelta for the duration
            arrival_time='10:00:00',
            plane='Plane123',
            airline='AirlineABC',
            economy_fare=100.0,
            business_fare=200.0,
            first_fare=300.0
        )
        self.flight.depart_day.add(self.week)  # Add the week to the flight

        # Create a test ticket
        self.ticket = Ticket.objects.create(
            user=self.user,
            ref_no='TICKET123',
            flight=self.flight,
            flight_ddate='2024-08-20',
            flight_adate='2024-08-20',
            flight_fare=100.0,
            other_charges=10.0,
            coupon_used='COUPON',
            coupon_discount=5.0,
            total_fare=105.0,
            seat_class='economy',
            mobile='1234567890',
            email='testuser@example.com',
            status='CONFIRMED'
        )
        
        # Create a test client
        self.client = Client()

    def test_get_ticket_success(self):
        response = self.client.get(reverse('getticket'), {'ref': 'TICKET123'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertTrue(response.content.startswith(b'%PDF'))  # Check if the response starts with PDF header

    def test_get_ticket_invalid_ref(self):
        # Prueba con una referencia de ticket inválida
        response = self.client.get(reverse('getticket'), {'ref': 'INVALIDREF'})
        self.assertEqual(response.status_code, 404)  # O el código de estado adecuado si la referencia no se encuentra
        # Verifica el contenido de la respuesta, puede ser una página de error o un mensaje específico
        self.assertContains(response, "Not Found")  # O el mensaje que esperas ver en caso de referencia inválida

    # def test_get_ticket_missing_ref(self):
    #     response = self.client.get(reverse('getticket'))
    #     self.assertEqual(response.status_code, 500)  # Assuming a 500 error for missing ref parameter
    #     self.assertIn(b'Internal Server Error', response.content)  # Check if the error page content is present

    # def test_get_ticket_without_authentication(self):
    #     # This test might not be applicable if the view doesn't require authentication
    #     response = self.client.get(reverse('getticket'), {'ref': 'TICKET123'})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response['Content-Type'], 'application/pdf')
    #     self.assertTrue(response.content.startswith(b'%PDF'))  # Check if the response starts with PDF header