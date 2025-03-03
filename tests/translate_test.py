import unittest
from unittest.mock import patch
from offices_translate import MoneyForMonth


class TestMoneyForMonth(unittest.TestCase):
    @patch.object(MoneyForMonth, 'request_email')
    def test_request_summ_no_message(self, mock_request_email):
        money_for_month = MoneyForMonth(data=['2', '1'])
        mock_request_email.return_value = []
        result = money_for_month.request_summ()
        self.assertEqual(result, "За указанный период расчетов не было")

    @patch.object(MoneyForMonth, 'request_email')
    def test_request_summ_message(self, mock_request_email):
        money_for_month = MoneyForMonth(data=['2', '1'])
        mock_request_email.return_value =  [['243982', '2025-02-03 10:12:10+03:00', ('test1@test.com',), '\n150 гривен\n\xa0\n\xa0']]
        result = money_for_month.request_summ()
        self.assertIn('150',result)

if __name__ == '__main__':
    unittest.main()

