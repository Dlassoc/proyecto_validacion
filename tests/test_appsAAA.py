from django.test import TestCase
from django.apps import apps
from flight.apps import FlightConfig  # Asegúrate de que la importación es correcta

class FlightConfigTest(TestCase):
    def test_app_config(self):
        # Arrange
        # Obtiene la configuración de la aplicación a través del nombre
        flight_config = apps.get_app_config('flight')

        # Assert
        self.assertEqual(flight_config.name, FlightConfig.name)  # Verifica que el nombre sea correcto
