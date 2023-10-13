import unittest
from utils.conversionFunctions import convert_market_cap

class TestConvertMarketCap(unittest.TestCase):

    def test_convert_millions(self):
        result = convert_market_cap("116.624M")
        print("Expected:", 116.624 * 1e6, "Got:", result)
        self.assertEqual(result, 116.624 * 1e6)

        result = convert_market_cap("1M")
        print("Expected:", 1e6, "Got:", result)
        self.assertEqual(result, 1e6)

        result = convert_market_cap("0.5M")
        print("Expected:", 0.5 * 1e6, "Got:", result)
        self.assertEqual(result, 0.5 * 1e6)

    def test_convert_billions(self):
        result = convert_market_cap("2.5B")
        print("Expected:", 2.5 * 1e9, "Got:", result)
        self.assertEqual(result, 2.5 * 1e9)
        self.assertEqual(convert_market_cap("2.5B"), 2.5 * 1e9)
        self.assertEqual(convert_market_cap("1B"), 1e9)
        self.assertEqual(convert_market_cap("0.1B"), 0.1 * 1e9)

    def test_convert_trillions(self):
        self.assertEqual(convert_market_cap("1T"), 1e12)
        self.assertEqual(convert_market_cap("0.5T"), 0.5 * 1e12)

    def test_without_suffix(self):
        self.assertEqual(convert_market_cap("1000"), 1000.0)
        self.assertEqual(convert_market_cap("1,000"), 1000.0)

    def test_invalid_values(self):
        self.assertIsNone(convert_market_cap("1Z"))  # Unrecognized suffix
        self.assertIsNone(convert_market_cap("ABC"))  # Non-numeric string

if __name__ == "__main__":
    unittest.main()