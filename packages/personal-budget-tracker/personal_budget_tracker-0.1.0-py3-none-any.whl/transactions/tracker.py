from datetime import datetime

#Это класс для одной транзакции, например доход или расход
class Transactions:
    def __init__(self, amount, category, date=None):
        """
        Инициализирует транзакцию.
        Перое - это сумма транзакции, для расходов
        потом категория, типо такси или еда
        потом дата, по умолчанию текущ время, поэтому и импортровали библ
        """
        self.amount = amount
        self.category = category
        self.date = date or datetime.now()

#для управления списком транзакций
class BudgetTracker:
    def __init__(self):
        """
        создает объект для отслеживания бюджета
        изначально список пуст
        """
        self.transactions = []

    def add_transaction(self, amount, category):
        """
        добавляет новую транзакцию,
        сумма транзакции и категория транзакции
        """
        self.transactions.append(Transactions(amount, category))

    def calculate_balance(self):
        """
        вычисляем общий баланс
        """
        return sum(t.amount for t in self.transactions)
    

#ЭТО ЧТОБЫ ИМОПРТ НОРМ БЫЛ ДЛЯ ТЕСТА
tracker = BudgetTracker()

def add_transaction(amount, category, date=None):
  tracker.add_transaction(amount, category, date)


def calculate_balance():
  return tracker.calculate_balance()