import unittest
from datetime import datetime, timedelta
from decimal import Decimal
import sqlite3

from finance_app.api.cache import get_cached_price, store_price
from finance_app.database.queries import create_tables


class TestCache(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.connection.row_factory = sqlite3.Row
        create_tables(self.connection)

    def tearDown(self):
        self.connection.close()

    def test_cached_price_fresh(self):
        now = datetime.utcnow()
        store_price(self.connection, "AAPL", Decimal("100"), now)

        cached = get_cached_price(self.connection, "AAPL", 60, now)
        self.assertIsNotNone(cached)
        self.assertEqual(cached.preco, Decimal("100"))

    def test_cached_price_expired(self):
        now = datetime.utcnow()
        past = now - timedelta(seconds=120)
        store_price(self.connection, "AAPL", Decimal("100"), past)

        cached = get_cached_price(self.connection, "AAPL", 60, now)
        self.assertIsNone(cached)


if __name__ == "__main__":
    unittest.main()
