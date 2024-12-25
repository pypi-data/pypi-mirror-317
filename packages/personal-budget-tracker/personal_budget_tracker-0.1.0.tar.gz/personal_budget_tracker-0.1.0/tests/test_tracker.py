import unittest
from transactions.tracker import Transactions, BudgetTracker
# from transactions.models import Transaction

class TestTracker(unittest.TestCase):
    #Убедимся что функция add_transaction корректно добавляет транзакцию в список транзакций.
    def test_add_transaction(self):
        transactions = [] #создаем пустой список
        b = BudgetTracker(-100, 'Food') #добавляем
        b.add_transactions()
        self.assertIn(t, transactions) #провверяем что находится внутри

    def test_calculate_balance(self):
        transactions = [
            Transactions(-100, 'Food', '2024-12-01'),
            Transactions(200, 'Salary', '2024-12-02')
        ]
        balance = calculate_balance(transactions)
        self.assertEqual(balance, 100)
