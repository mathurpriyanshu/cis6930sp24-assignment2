import unittest
from assignment2 import get_lat_lon_from_location, calculate_bearing, determine_side_of_town

class TestGeoFunctions(unittest.TestCase):

    def test_get_lat_lon_from_location(self):
        lat, lon = get_lat_lon_from_location("New York City")
        self.assertAlmostEqual(lat, 40.7128, places=4)
        self.assertAlmostEqual(lon, -74.0060, places=4)

    def test_calculate_bearing(self):
        bearing = calculate_bearing(35.2226, -97.4395, 40.7128, -74.0060)  # Norman, OK to NYC
        self.assertAlmostEqual(bearing, 59.2404, places=1)

    def test_determine_side_of_town(self):
        side = determine_side_of_town(59.2404)  # Assuming bearing for NYC
        self.assertEqual(side, "NE")  # NYC is Northeast of Norman, OK

if __name__ == '__main__':
    unittest.main()
