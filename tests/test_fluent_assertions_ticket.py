import json
from datetime import time, timedelta
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from flight.models import Ticket, Flight, Place

class TicketDataTest(TestCase):

    @patch('flight.models.Ticket.objects.get')
    def test_ticket_data(self, mock_get):
        origin = Place(code="NYC")
        origin.save()
        
        destination = Place(code="LAX")
        destination.save()

        flight = Flight(
            origin=origin,
            destination=destination,
            depart_time=time(10, 0),  
            duration=timedelta(hours=2),  
            arrival_time=time(12, 0),  
            plane="FL123",
            airline="Airline Example",
            economy_fare=200.0,
            business_fare=400.0,
            first_fare=600.0
        )
        flight.save()
        
        ticket = Ticket(
            ref_no="ABC123",
            flight=flight,
            flight_ddate="2024-10-01",
            status="CONFIRMED"
        )
        ticket.save()

        mock_get.return_value = ticket

        response = self.client.get(reverse('ticketdata', args=['ABC123']))
        self.assertEqual(response.status_code, 200)
        
        response_data = json.loads(response.content)
        self.assertEqual(response_data['ref'], ticket.ref_no)
        self.assertEqual(response_data['from'], ticket.flight.origin.code)
        self.assertEqual(response_data['to'], ticket.flight.destination.code)
        self.assertEqual(response_data['flight_date'], str(ticket.flight_ddate))
        self.assertEqual(response_data['status'], ticket.status)

if __name__ == '__main__':
    unittest.main()
