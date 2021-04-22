import unittest
from datetime import datetime

from main import form_date


class MyTestCase(unittest.TestCase):
    def test_user_date(self):
        self.assertEqual(form_date(2020, 12, 31, 12, 12), datetime(2020, 12, 31, 12, 12).strftime("%Y%m%d%H%M"))

    def test_current_date(self):
        date = datetime.now()

        year = date.year
        month = date.month
        day = date.day
        hour = date.hour
        minute = date.minute

        self.assertEqual(form_date(), datetime(year, month, day, hour, minute).strftime("%Y%m%d%H%M"))

    def test_result_day(self):
        self.assertEqual(form_date(2021, 12, 31, 23, 59), "202112312359")


if __name__ == '__main__':
    unittest.main()
