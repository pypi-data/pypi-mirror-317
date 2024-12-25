import unittest
from analysis.analytics import analyze_expenses_by_category, find_highest_expense_category
from transactions.models import Transaction

class TestAnalytics(unittest.TestCase):
    def test_analyze_expenses_by_category(self):
        transactions = [
            Transaction(-100, 'Food', '2024-12-01'),
            Transaction(-50, 'Transport', '2024-12-02'),
            Transaction(-200, 'Food', '2024-12-03')
        ]
        result = analyze_expenses_by_category(transactions)
        self.assertEqual(result, {'Food': 300.0, 'Transport': 50.0})

    def test_find_highest_expense_category(self):
        transactions = [
            Transaction(-100, 'Food', '2024-12-01'),
            Transaction(-50, 'Transport', '2024-12-02'),
            Transaction(-200, 'Food', '2024-12-03')
        ]
        highest = find_highest_expense_category(transactions)
        self.assertEqual(highest, 'Food')
