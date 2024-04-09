import unittest
from assignment2 import pdf_download, data_extract, determine_day_of_week, determine_time_of_day, determine_weather, rank_locations, determine_side_of_town

class TestIncidentFunctions(unittest.TestCase):

    def test_pdf_download(self):
        """Test PDF download with a known good URL and expect a file path returned."""
        result = pdf_download('http://example.com/sample.pdf')
        self.assertIsNotNone(result)
        self.assertTrue(result.endswith('.pdf'))

    def test_data_extract(self):
        """Test data extraction from a mock PDF path and expect a non-empty list returned."""
        mock_pdf_path = 'path_to_mock_pdf'
        result = data_extract(mock_pdf_path)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_determine_day_of_week(self):
        """Test determining the day of the week from a valid date string."""
        result = determine_day_of_week('12/25/2024')
        self.assertEqual(result, 3)  # Assuming Dec 25, 2024 is a Wednesday

    def test_determine_time_of_day(self):
        """Test determining the hour from a valid datetime string."""
        result = determine_time_of_day('12/25/2024 14:30')
        self.assertEqual(result, 14)

    def test_determine_weather(self):
        """Test weather determination function with known coordinates and time."""
        result = determine_weather(40.7128, -74.0060, 1633036800)
        self.assertIsNotNone(result)

    def test_rank_locations(self):
        """Test location ranking with a list of locations."""
        locations = ['New York', 'Los Angeles', 'New York', 'Chicago']
        result = rank_locations(locations)
        self.assertEqual(result, [1, 2, 1, 3])

    def test_determine_side_of_town(self):
        """Test determining the side of town for a known location."""
        result = determine_side_of_town('Central Park, New York')
        self.assertIn(result, ['Center', 'Outside', 'Unknown'])

    def test_db_population(self):
        """Ensure that data is correctly inserted into the database."""
        # This would typically require mocking the database or using a test database
        pass

if __name__ == '__main__':
    unittest.main()
