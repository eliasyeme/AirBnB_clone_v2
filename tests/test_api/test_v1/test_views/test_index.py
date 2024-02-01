import unittest
from flask import Flask, jsonify
from api.v1.app import teardown
from api.v1.views.index import app_views


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(app_views)

    def test_status(self):
        with self.app.test_client() as client:
            response = client.get("/status")
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data["status"], "OK")

    def tearDown(self):
        teardown(None)


if __name__ == "__main__":
    unittest.main()
