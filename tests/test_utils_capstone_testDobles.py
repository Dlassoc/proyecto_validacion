from django.http import HttpResponse
from unittest import TestCase
from unittest.mock import patch, Mock
from capstone.utils import render_to_pdf


class RenderToPdfTest(TestCase):

    @patch("capstone.utils.pisa.pisaDocument")
    @patch("capstone.utils.get_template")
    def test_render_to_pdf_success(self, mock_get_template, mock_pisa_document):
        mock_template = Mock()
        mock_template.render.return_value = "<html></html>"
        mock_get_template.return_value = mock_template

        mock_pisa_document.return_value.err = False

        response = render_to_pdf("dummy_template.html", {})

        mock_get_template.assert_called_once_with("dummy_template.html")

        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    @patch("capstone.utils.pisa.pisaDocument")
    @patch("capstone.utils.get_template")
    def test_render_to_pdf_failure(self, mock_get_template, mock_pisa_document):
        mock_template = Mock()
        mock_template.render.return_value = "<html></html>"
        mock_get_template.return_value = mock_template

        mock_pisa_document.return_value.err = True

        response = render_to_pdf("dummy_template.html", {})

        self.assertIsNone(response)


