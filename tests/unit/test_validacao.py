import unittest
from datetime import date
from decimal import Decimal

from finance_app.utils.validacao import validate_date, validate_non_empty, validate_positive


class TestValidacao(unittest.TestCase):
    def test_validate_non_empty(self):
        self.assertEqual(validate_non_empty(" ok ", "campo"), "ok")

    def test_validate_non_empty_raises(self):
        with self.assertRaises(ValueError):
            validate_non_empty("", "campo")

    def test_validate_positive(self):
        self.assertEqual(validate_positive(Decimal("1.0"), "valor"), Decimal("1.0"))

    def test_validate_positive_raises(self):
        with self.assertRaises(ValueError):
            validate_positive(Decimal("0"), "valor")

    def test_validate_date(self):
        value = date.today()
        self.assertEqual(validate_date(value, "data"), value)


if __name__ == "__main__":
    unittest.main()
