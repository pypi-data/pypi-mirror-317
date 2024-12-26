import unittest
from LLMsWebScraper import LLMsWebScraper

class TestLLMWebScraper(unittest.TestCase):
    def test_scraper_initialization(self):
        scraper = LLMsWebScraper(api_key="Gemini_API_KEY")
        self.assertIsNotNone(scraper)

    # Add more test cases as needed

if __name__ == "__main__":
    unittest.main()
