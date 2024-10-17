from io import BytesIO
import unittest
from django.http import HttpResponse
from unittest import TestCase
from unittest.mock import patch, Mock, mock_open, MagicMock
from capstone.utils import render_to_pdf
from flight.models import Ticket, Flight, Place, Week
from capstone.utils import createticket
from datetime import datetime, timedelta
import secrets
from flight.utils import addInternationalFlights


class RenderToPdfTest(TestCase):

    @patch("capstone.utils.pisa.pisaDocument")
    @patch("capstone.utils.get_template")
    def test_render_to_pdf_success(self, mock_get_template, mock_pisa_document):
        # Mockeamos el template
        mock_template = Mock()
        # HTML ficticio para simular una plantilla renderizada
        mock_template.render.return_value = "<html></html>"
        mock_get_template.return_value = mock_template

        # Mockeamos pisaDocument para que no devuelva ningún error
        mock_pisa_document.return_value.err = False

        # Llamamos a la función con un contexto vacío
        response = render_to_pdf("dummy_template.html", {})

        # Verificamos que se llama a get_template con el template correcto
        mock_get_template.assert_called_once_with("dummy_template.html")

        # Verificamos que la función retorna un HttpResponse con content_type PDF
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    @patch("capstone.utils.pisa.pisaDocument")
    @patch("capstone.utils.get_template")
    def test_render_to_pdf_failure(self, mock_get_template, mock_pisa_document):
        # Mockeamos el template
        mock_template = Mock()
        mock_template.render.return_value = "<html></html>"
        mock_get_template.return_value = mock_template

        # Simulamos que hay un error en la conversión a PDF
        mock_pisa_document.return_value.err = True

        # Llamamos a la función y verificamos que retorna None en caso de error
        response = render_to_pdf("dummy_template.html", {})

        self.assertIsNone(response)


