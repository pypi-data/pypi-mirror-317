import datetime
import unittest

from mokeidb.serializer import Serializer


class TestSerializer(unittest.TestCase):
    def test_serialize(self):
        serializer = Serializer()
        self.assertEqual('2021-12-25', serializer.to_dict(datetime.date(2021, 12, 25)))
        self.assertEqual(datetime.date(2021, 12, 25), serializer.from_dict(datetime.date, '2021-12-25'))
