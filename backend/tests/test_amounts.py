import unittest

from services.amounts import format_wei_as_eth, format_units

class AmountFormattingTests(unittest.TestCase):
    def test_zero_balance(self):
        result = format_wei_as_eth(0)
        self.assertEqual(result, "0")

    def test_one_wei(self):
        result = format_wei_as_eth(1)
        self.assertEqual(result, "0.000000000000000001")

    def test_one_eth(self):
        result = format_wei_as_eth(10**18)
        self.assertEqual(result, "1")

    def test_half_eth(self):
        result = format_wei_as_eth(5 * 10**17)
        self.assertEqual(result, "0.5")

    def test_full_precision(self):
        result = format_wei_as_eth(1234567890123456789)
        self.assertEqual(result, "1.234567890123456789")

    def test_large_balance(self):
        result = format_wei_as_eth(123456789012345678901234567890)
        self.assertEqual(result, "123456789012.34567890123456789")

    def test_negative_balance(self):
        with self.assertRaises(ValueError):
            format_wei_as_eth(-1)

class UnitFormattingTests(unittest.TestCase):
    def test_six_decimals(self):
        result = format_units(1234567, decimals=6)
        self.assertEqual(result, "1.234567")

    def test_smallest_unit(self):
        result = format_units(1, decimals=6)
        self.assertEqual(result, "0.000001")

    def test_zero_decimals(self):
        result = format_units(1234567, decimals=0)
        self.assertEqual(result, "1234567")

    def test_remove_trailing_zeros(self):
        result = format_units(1200000, decimals=6)
        self.assertEqual(result, "1.2")

    def test_zero_amount(self):
        result = format_units(0, decimals=6)
        self.assertEqual(result, "0")

    def test_negative_amount(self):
        with self.assertRaises(ValueError):
            format_units(-1, decimals=6)

    def test_negative_decimals(self):
        with self.assertRaises(ValueError):
            format_units(1, decimals=-1)

    def test_decimals_above_limit(self):
        with self.assertRaises(ValueError):
            format_units(1, decimals=256)

    def test_maximum_decimals(self):
        result = format_units(1, decimals=255)
        expected = "0." + "0" * 254 + "1"
        self.assertEqual(result, expected)