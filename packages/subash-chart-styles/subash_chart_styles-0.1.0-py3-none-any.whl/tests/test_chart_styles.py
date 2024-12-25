# tests/test_chart_styles.py
import unittest
from subash_chart_styles.chart_styles import format_large_numbers

class TestChartStyles(unittest.TestCase):
    def test_format_large_numbers(self):
        self.assertEqual(format_large_numbers(1000000000, None), "$1.0B")
        self.assertEqual(format_large_numbers(1500000, None), "$1.5M")
        self.assertEqual(format_large_numbers(0, None), "$0")

if __name__ == '__main__':
    unittest.main()
