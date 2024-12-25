import unittest
from analysis.visualization import plot_expenses_by_category
from transactions.models import Transaction
import os

class TestVisualization(unittest.TestCase):
    def test_plot_expenses_by_category(self):
        transactions = [
            Transaction(-100, 'Food', '2024-12-01'),
            Transaction(-50, 'Transport', '2024-12-02')
        ]
        filepath = "test_plot.png" #сохраняем график
        plot_expenses_by_category(transactions, filepath) #вызываем функцию
        self.assertTrue(os.path.exists(filepath)) #проверяем что файл был создан
        os.remove(filepath)  # Удаляем файл после проверки
