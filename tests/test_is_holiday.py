import unittest
from utils.is_holiday import is_holiday


class TestIsHoliday(unittest.TestCase):
    def test_known_holiday(self):
        # Test with a date that is a known US federal holiday
        self.assertTrue(is_holiday("2024-01-01"))  # New Year's Day 2024
        print(f"Expected: {True}, Got: {is_holiday('2024-01-01')}")

    def test_known_non_holiday(self):
        # Test with a date that is not a US federal holiday
        self.assertFalse(is_holiday("2024-01-02"))  # Day after New Year's Day 2024
        print(f"Expected: {False}, Got: {is_holiday('2024-01-02')}")


if __name__ == "__main__":
    unittest.main()
