import unittest
from utils.conversionFunctions import clean_and_convert

class TestCleanAndConvert(unittest.TestCase):
    def test_clean_and_convert(self):
        values = ["5", 50, "100", "1,086", "10000", "3,403.43", "10.23"]
        expected_results = [5, 50, 100, 1086, 10000, 3403.43, 10.23]
        
        for val, expected in zip(values, expected_results):
            result = clean_and_convert(val)
            print(f"clean_and_convert({val!r}) = {result!r}")
            self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()