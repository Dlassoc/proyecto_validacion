import unittest
from unittest.mock import patch, mock_open
import os
from django.test import TestCase
from flight.utils import get_number_of_lines, createWeekDays, addPlaces
from flight.models import Week, Place  


class TestGetNumberOfLines(unittest.TestCase):

    def setUp(self):
        # Arrange
        self.empty_file = 'empty_file.txt'
        self.single_line_file = 'single_line_file.txt'
        self.multi_line_file = 'multi_line_file.txt'

        with open(self.empty_file, 'w') as f:
            pass

        with open(self.single_line_file, 'w') as f:
            f.write('This is a single line.\n')  # Archivo con una sola línea

        with open(self.multi_line_file, 'w') as f:
            f.write('Line 1\nLine 2\nLine 3\n')  # Archivo con varias líneas

    def tearDown(self):
        os.remove(self.empty_file)
        os.remove(self.single_line_file)
        os.remove(self.multi_line_file)

    def test_empty_file(self):
        # Act
        result = get_number_of_lines(self.empty_file)
        # Assert
        self.assertEqual(result, 0)


def test_single_line_file(self):
    # Act
    result = get_number_of_lines(self.single_line_file)
    print(f"Number of lines in single_line_file: {result}")  # Debug
    # Assert
    self.assertEqual(result, 1)

    def test_multi_line_file(self):
        # Act
        result = get_number_of_lines(self.multi_line_file)
        # Assert
        self.assertEqual(result, 3)


class TestCreateWeekDays(TestCase):

    def setUp(self):
        # Arrange
        Week.objects.all().delete()

    def test_create_week_days(self):
        # Act
        createWeekDays()

        # Assert
        self.assertEqual(Week.objects.count(), 7)

        expected_days = [
            ('Monday', 0),
            ('Tuesday', 1),
            ('Wednesday', 2),
            ('Thursday', 3),
            ('Friday', 4),
            ('Saturday', 5),
            ('Sunday', 6),
        ]

        for name, number in expected_days:
            week_day = Week.objects.get(number=number)
            self.assertEqual(week_day.name, name)


class TestAddPlaces(TestCase):

    def setUp(self):
        # Arrange
        Place.objects.all().delete()

    @patch("builtins.open", new_callable=mock_open, read_data="City,Airport,Code,Country\nNew York,JFK,JFK,USA\nLos Angeles,LAX,LAX,USA")
    @patch("flight.utils.get_number_of_lines", return_value=3)
    def test_add_places(self, mock_get_number_of_lines, mock_open):
        # Act
        addPlaces()
        # Assert
        self.assertEqual(Place.objects.count(), 2)

        new_york = Place.objects.get(city='New York')
        self.assertEqual(new_york.airport, 'JFK')
        self.assertEqual(new_york.code, 'JFK')
        self.assertEqual(new_york.country, 'USA')

        los_angeles = Place.objects.get(city='Los Angeles')
        self.assertEqual(los_angeles.airport, 'LAX')
        self.assertEqual(los_angeles.code, 'LAX')
        self.assertEqual(los_angeles.country, 'USA')


if __name__ == '__main__':
    unittest.main()
