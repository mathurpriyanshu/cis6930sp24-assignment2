import unittest
from assignment2 import calculate_incident_ranks, check_emsstat

class TestNatureFunctions(unittest.TestCase):

    def test_calculate_incident_ranks(self):
        incidents = [
            ["03/21/2024 08:30", "Sunny", "Location1", "Nature1", "EMSSTAT"],
            ["03/21/2024 09:30", "Cloudy", "Location2", "Nature2", "NoEMS"]
        ]
        ranks = calculate_incident_ranks(incidents)
        self.assertEqual(ranks["Nature1"], 1)
        self.assertEqual(ranks["Nature2"], 2)

    def test_check_emsstat(self):
        incidents = [
            ["03/21/2024 08:30", "Sunny", "Location1", "Nature1", "EMSSTAT"],
            ["03/21/2024 08:30", "Cloudy", "Location2", "Nature2", "NoEMS"],
            ["03/21/2024 08:30", "Rainy", "Location3", "Nature3", "EMSSTAT"]
        ]
        self.assertTrue(check_emsstat(incidents[0], incidents, 0))
        self.assertFalse(check_emsstat(incidents[1], incidents, 1))
        self.assertTrue(check_emsstat(incidents[2], incidents, 2))

if __name__ == '__main__':
    unittest.main()
