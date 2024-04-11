import unittest
from assignment2 import get_day_of_week, get_time_of_day

class TestTimeFunctions(unittest.TestCase):

    def test_get_day_of_week(self):
        self.assertEqual(get_day_of_week("03/21/2024 08:30"), 4)  # Thursday

    def test_get_time_of_day(self):
        self.assertEqual(get_time_of_day("03/21/2024 08:30"), 8)  # 8 AM

if __name__ == '__main__':
    unittest.main()
