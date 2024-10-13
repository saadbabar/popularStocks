from django.test import TestCase
from wsbAnalysis.reddit import fetch_company_tickers, clean_name

# Create your tests here.
class FetchCompanyTickersTest(TestCase):
    def setUp(self):
        pass

    def test_clean_company_name(self):
        self.assertEqual(clean_name('APPLE INC'), 'apple')

    def test_find_companies(self):
        output = fetch_company_tickers()
        self.assertIn('apple', output)
        self.assertIn('tesla', output)