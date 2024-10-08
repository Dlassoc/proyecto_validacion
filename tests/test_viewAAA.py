from django.test import TestCase
from django.urls import reverse


class AboutUsViewTest(TestCase):
    def test_about_us_view(self):
        # Arrange
        url = reverse('aboutus')

        # Act
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flight/about.html')

class ContactViewTest(TestCase):

    def test_contact_view(self):
        # Arrange
        url = reverse('contact')

        # Act
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flight/contact.html')


class PrivacyPolicyViewTest(TestCase):
    def test_privacy_policy_view(self):
        # Arrange
        url = reverse('privacypolicy')

        # Act
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flight/privacy-policy.html')


class TermsAndConditionsViewTest(TestCase):
    def test_terms_and_conditions_view(self):
        # Arrange
        url = reverse('termsandconditions')

        # Act
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flight/terms.html')
