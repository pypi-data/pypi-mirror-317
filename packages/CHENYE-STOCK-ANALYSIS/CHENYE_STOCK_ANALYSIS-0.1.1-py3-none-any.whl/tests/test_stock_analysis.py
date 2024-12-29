import unittest
from stock_analysis import DataFetcher

class TestStockAnalyzer(unittest.TestCase):
    def test_find_recent_trading_day(self):
        analyzer = DataFetcher()
        recent_day = analyzer.find_recent_trading_day()
        self.assertTrue(recent_day.isdigit() and len(recent_day) == 8)
        analyzer.logout()

if __name__ == "__main__":
    unittest.main()