from collections import defaultdict

#Анализируем траты по категориям
def analyze_expenses_by_category(transactions):
    """
    список транзакций и словарь, где ключ — категория, значение — сумма расходов.
    """
    category_totals = defaultdict(float)  
    for t in transactions:
        #если сумма отрицательная, то есть расход, добавляем по модулю
        if t.amount < 0:  
            category_totals[t.category] += abs(t.amount)
    return category_totals

# Функция поиска самой дорогой категории
def find_highest_expense_category(transactions):
    """
    список объектов транзакшионс, с информацией о сумме, категории и дате
    сначала анализируем список транзакций и возвращаем словарь
    category_totals.get - значит что мы должны учитывать значения
    если словарь пустой, вернет Нон
    ну и вернет название категории (ключ словаря)
    """
    category_totals = analyze_expenses_by_category(transactions)
    return max(category_totals, key=category_totals.get, default=None)