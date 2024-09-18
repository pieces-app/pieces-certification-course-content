# tests/test_app.py
import unittest
from app import app

class PageLoadTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    # executed after each test
    def tearDown(self):
        self.app_context.pop()

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your home for the best Sci-Fi inspired toys', response.data)

    def test_about_page(self):
        response = self.app.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Soon we will be selling a range of plushie toys', response.data)

if __name__ == "__main__":
    unittest.main()
