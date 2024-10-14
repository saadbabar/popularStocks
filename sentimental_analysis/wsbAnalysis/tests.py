from django.test import TestCase
from wsbAnalysis.reddit import fetch_company_tickers, clean_name, extract_stock_symbol, remove_stopwords, filtered_sentence, fetch_fmp_company_tickers
from .data import fmp_key
import pdbp

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

    def test_remove_stopwords(self):
        sentence1 = "You are a great person but this is not important."
        self.assertEqual(remove_stopwords(sentence1), "great person important.")

    def test_extract_stock_symbol(self):
        output = fetch_company_tickers
        sentence1 = 'I think $AAPL to the moon'
        sentence2 = remove_stopwords('What do you guys think Microsoft is going to do')
        sentence3 = 'rklb is cooked'
        sentence4 = 'what about Boeing'
        sentence5 = filtered_sentence("Bought 150k rivian, failing ev company")

        # breakpoint()
        self.assertEqual(extract_stock_symbol(sentence1), 'AAPL')
        # breakpoint()
        self.assertEqual(extract_stock_symbol(sentence2), 'MSFT')
        self.assertEqual(extract_stock_symbol(sentence3), 'RKLB')
        # breakpoint()
        self.assertEqual(extract_stock_symbol(sentence4), 'BA')
        # breakpoint()
        self.assertEqual(extract_stock_symbol(sentence5), 'RIVN')

    def test_filtered_sentence(self):
        sentence1 = 'Boeing’s Endless Doom Loop Gives Respite New CEO'
        # breakpoint()
        self.assertEqual(filtered_sentence(sentence1),'Boeing Endless Doom Loop Gives Respite New CEO')

    def test_fmp_tikcers(self):
        result = fetch_fmp_company_tickers(fmp_key)
        print(result)
        self.assertIn('tesla', result)
        self.assertIn('intuitive machines', result)
        self.assertIn('rivian', result)
        self.assertIn('boeing', result)
        
