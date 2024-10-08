from django.test import TestCase, RequestFactory
from django.http import HttpResponse
from unittest.mock import patch
from datetime import datetime
from flight.models import Ticket
from flight.views import get_ticket


class GetTicketViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.ticket = Ticket.objects.create(ref_no="ABC123")

    @patch("flight.views.render_to_pdf")
    def test_get_ticket_success(self, mock_render_to_pdf):
        # Arrange
        mock_render_to_pdf.return_value = b"PDF content"
        request = self.factory.get("/get-ticket/?ref=ABC123")

        # Act
        response = get_ticket(request)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertEqual(response.content, b"PDF content")

    def test_get_ticket_no_ref(self):
        # Arrange
        request = self.factory.get("/get-ticket/")

        # Act
        response = get_ticket(request)

        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(),
                         "Reference number is required.")

    def test_get_ticket_not_found(self):
        # Arrange
        request = self.factory.get("/get-ticket/?ref=XYZ999")

        # Act
        response = get_ticket(request)

        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content.decode(), "Ticket not found.")
