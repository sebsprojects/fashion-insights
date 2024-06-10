import sys
import unittest

if __name__ == "__main__":
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover("tests")
    test_runner = unittest.TextTestRunner()
    result = test_runner.run(test_suite)
    if not result.wasSuccessful():
        sys.exit(1)
