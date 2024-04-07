import unittest
import os

if __name__ == "__main__":
    # Automatically discover all tests in the 'tests' directory
    print("Running tests...")
    print(f"Looking for tests in: {os.path.abspath('tests')}")

    loader = unittest.TestLoader()
    suite = loader.discover("tests", pattern="test_*.py")
    print(f"Found {suite.countTestCases()} tests")

    # Run the test suite
    runner = unittest.TextTestRunner()
    runner.run(suite)
