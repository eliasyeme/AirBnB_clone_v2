import unittest
from flask import Flask
from api.v1.app import teardown


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)

    def test_teardown(self):
        with self.app.app_context():
            # Ensure that the storage is closed
            teardown(None)
            # Add your assertions here to test the behavior of the teardown function


if __name__ == "__main__":
    unittest.main()
