from django.test import TestCase
from django.urls import reverse
from datetime import datetime
from flight.models import Place, Flight, Week

class FlightSearchTestCase(TestCase):

    def setUp(self):
        # Crea los lugares de origen y destino
        self.origin = Place.objects.create(city="Paris", airport="Charles de Gaulle", code="CDG", country="France")
        self.destination = Place.objects.create(city="Dubai", airport="Dubai International", code="DXB", country="UAE")

        # Crea el día de la semana basado en la fecha de salida
        depart_date = datetime.strptime("2024-09-17", "%Y-%m-%d")
        self.weekday = Week.objects.create(number=depart_date.weekday(), name="Tuesday")

        # Crea un vuelo de ejemplo en clase 'business'
        self.flight = Flight.objects.create(
            origin=self.origin,
            destination=self.destination,
            depart_time="09:00:00",
            arrival_time="15:00:00",
            plane="Boeing 777",
            airline="Emirates",
            business_fare=500
        )
        self.flight.depart_day.add(self.weekday)  

        # Imprime los detalles del vuelo para verificar que se ha creado correctamente
        print("Detalles del vuelo creado:")
        print(f"ID: {self.flight.id}")
        print(f"Origen: {self.flight.origin}")
        print(f"Destino: {self.flight.destination}")
        print(f"Hora de salida: {self.flight.depart_time}")
        print(f"Hora de llegada: {self.flight.arrival_time}")
        print(f"Aeroplano: {self.flight.plane}")
        print(f"Aerolínea: {self.flight.airline}")
        print(f"Precio en clase business: {self.flight.business_fare}")
        print(f"Día de salida: {', '.join(str(day) for day in self.flight.depart_day.all())}")

    def test_flight_search_business_class(self):
        # Realiza una petición GET simulada
        response = self.client.get(reverse('flight'), {
            'Origin': 'CDG',
            'Destination': 'DXB',
            'DepartDate': '2024-09-17',
            'SeatClass': 'business',
            'TripType': '1'  # Solo ida
        })

        # Verifica que la respuesta fue exitosa (HTTP 200)
        self.assertEqual(response.status_code, 200)

        # Verifica que el contexto contiene el vuelo esperado
        flights = response.context['flights']
        self.assertEqual(len(flights), 1)
        
        # Compara campos individuales en lugar del objeto completo
        flight = flights[0]
        self.assertEqual(flight.origin.code, 'CDG')
        self.assertEqual(flight.destination.code, 'DXB')
        self.assertEqual(flight.business_fare, 500)

        # Verifica los precios mínimo y máximo en clase 'business'
        self.assertEqual(response.context['min_price'], 500)
        self.assertEqual(response.context['max_price'], 500)

        # Verifica que la página contiene los detalles correctos del vuelo
        self.assertContains(response, 'Paris')
        self.assertContains(response, 'Dubai')
        self.assertContains(response, 'Business')
