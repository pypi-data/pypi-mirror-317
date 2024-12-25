import matplotlib.pyplot as plt

#Строим столбчатую диаграмму расходов по категориям
def plot_expenses_by_category(transactions):
    categories = {}
    for t in transactions:
        if t.amount < 0:
            #.get -- подучаем знач из словаря, если существует берем, если нет 0.то есть старое плюс новое
            categories[t.category] = categories.get(t.category, 0) + abs(t.amount)

    if not categories:
        print("Ничего нет блин :(")
        return
    
#Построение диаграммы
    plt.bar(categories.keys(), categories.values(), color='skyblue')
    plt.xlabel('Категория')
    plt.ylabel('Сумма расходов')  # ось Y
    plt.title('Расходы по категориям')  
    plt.xticks(rotation=45)  # Поворачиваем подписи категорий
    plt.tight_layout()  # Убираем лишние отступы
    plt.show()