"""
Данные от магазинов

От 5% до 15% посетителей совершают покупку.
Средняя стоимость покупки — от 20 до 22 тысяч рублей.
Наценка — 20%.
Магазин работает 18 часов в сутки.
В магазине посменно работают 2 продавца.
Зарплата продавца — 50 000 рублей + 43% налогов.

Выручка за месяц = проходимость * количество раб.часов в день * доля посетителей/прохожих *
доля покупателей/посетителей * средняя стоимость покупки * наценка * кол-во рабочих дней в мес.

Расходы за месяц = стоимость аренды + кол-во продавцов * зарплата с налогами

Ожидаемая прибыльность = traffic * 18 * 1/225 * 0.1 * 21000 * 0.2 * 30 - (price + 2 * 50000 * 1.43)
"""

min_required_area = 40 # минимальная требуемая площадь
max_affordable_price = 190000 # максимально допустимая арендная ставка
third_ring_radius = 6.7 # максимальное расстояние от центра

open_hours_number = 18 # количество рабочих часов в сутки
traffic2visitors_average_ratio = 1 / 225 # средняя доля посетителей от числа прохожих
traffic2visitors_pessimistic_ratio = 1 / 300 # минимальная доля посетителей от числа прохожих
visitors2purchases_average_ratio = 0.1 # средняя доля покупателей от числа посетителей
visitors2purchases_pessimistic_ratio = 0.05 # минимальная доля покупателей от числа посетителей
average_order_value = 21000 # средняя стоимость покупки
average_order_value_pessimistic = 20000 # минимальная стоимость покупки
trade_margin = 0.2 # наценка
days_in_months = 30 # количество рабочих дней в месяц

# множитель для расчёта прибыльности в среднем сценарии
income_multiplier_average = (open_hours_number *
                             traffic2visitors_average_ratio *
                             visitors2purchases_average_ratio *
                             average_order_value *
                             trade_margin *
                             days_in_months)

# множитель для расчёта прибыльности в пессимистичном сценарии
income_multiplier_pessimistic = (open_hours_number *
                                 traffic2visitors_pessimistic_ratio *
                                 visitors2purchases_pessimistic_ratio *
                                 average_order_value_pessimistic *
                                 trade_margin *
                                 days_in_months)

number_of_employees = 2 # количество продавцов
employee_salary = 50000 # зарплата продавца
tax_multiplier = 1.43 # множитель для расчёта зарплаты с налогами

# зарплатная часть расходов
addition_to_expenses = number_of_employees * employee_salary * tax_multiplier

# минимальная ожидаемая прибыль
min_expected_profits = 500000

import pandas
import seaborn

realty_df = pandas.read_csv('yandex_realty_data.csv')

#print(realty_df)

unique_area_units = []
unique_offer_types = []
unique_commercial_types = []

#ищем уникальные значения столбца 'area_unit', чтоб понять единицу измерения
for unit in realty_df['area_unit']:
    if unit not in unique_area_units:
        unique_area_units.append(unit)
#print(unique_area_units)

#проверяем тип предложения
for offer_type in realty_df['offer_type']:
    if offer_type not in unique_offer_types:
        unique_offer_types.append(offer_type)
#print(unique_offer_types)

#проверяем типы аренды, тк нам нужна площать под магазин
for types in realty_df['commercial_type']:
    if types not in unique_commercial_types:
        unique_commercial_types.append(types)
#print(unique_commercial_types)

#проверяем расположение магазинов по широте/долготе и удаленности от центра(hue) c помощью диаграммы рассеяния
#seaborn.scatterplot(x=realty_df['longitude'], y=realty_df['latitude'], hue=realty_df['distance'])

#проверяем наличие конкурентов (hue)
seaborn.scatterplot(x=realty_df['longitude'], y=realty_df['latitude'], hue=realty_df['competitors'])

#смотрим проходимость
#seaborn.scatterplot(x=realty_df['longitude'], y=realty_df['latitude'], hue=realty_df['traffic'])

index = 5
"""Список критериев после исследования датасета

realty_df['floor'][index] == 1
realty_df['area'][index] >= 40
realty_df['price'][index] <= 190000
realty_df['commercial_type'][index] in ['FREE_PURPOSE', 'RETAIL']
realty_df['distance'][index] <= 6.7
realty_df['already_taken'][index] == 0
realty_df['competitors'][index] <= 1
"""
# списки для важных параметров
filtered_objects_area = []
filtered_objects_price = []
filtered_objects_traffic = []
filtered_objects_address = []
filtered_objects_profits = []  # возможная средняя прибыльность
filtered_objects_profits_min = [] # возможная минимальная прибыльность

for index in range(len(realty_df)):
    if (realty_df['floor'][index] == 1 and
        realty_df['area'][index] >= min_required_area and
        realty_df['price'][index] <= max_affordable_price and
        realty_df['commercial_type'][index] in ['FREE_PURPOSE', 'RETAIL'] and
        realty_df['distance'][index] <= third_ring_radius and
        realty_df['already_taken'][index] == 0 and
        realty_df['competitors'][index] <= 1):
        filtered_objects_area.append(realty_df['area'][index])
        filtered_objects_price.append(realty_df['price'][index])
        filtered_objects_traffic.append(realty_df['traffic'][index])
        filtered_objects_address.append(realty_df['address'][index])
        filtered_objects_profits.append(realty_df['traffic'][index] *
        income_multiplier_average - (realty_df['price'][index] +
        addition_to_expenses))

#узнаем, сколько объявлений сохранил фильтр
#print(len(filtered_objects_area))

# макс.прибыльность среди отфильтрованных объектов
#print(max(filtered_objects_profits))

# индекс объекта с макс.прибыльнотью
# max_profit = max(filtered_objects_profits)
# for index in range(len(filtered_objects_profits)):
#     if filtered_objects_profits[index] == max_profit:
#         print(index)

# объекты с прибыльностью более 500к
for index in range(len(filtered_objects_profits)):
    if filtered_objects_profits[index] > min_expected_profits:
        print(filtered_objects_price[index])
        print(filtered_objects_traffic[index])
        print(filtered_objects_address[index])
        print(filtered_objects_profits[index])
        print(filtered_objects_traffic[index] * income_multiplier_pessimistic -
        (filtered_objects_price[index] + addition_to_expenses))
        print('----------')

# финальная версия кода
realty_df['expenses'] = realty_df['price'] + 2 * 50000 * 1.43
realty_df['incomes_normal'] = realty_df['traffic'] * 18 * 1/225 * 0.1 * 21000 * 0.2 * 30
realty_df['incomes_pessimistic'] = realty_df['traffic'] * 18 * 1/300 * 0.05 * 20000 * 0.2 * 30
realty_df['profits_normal'] = realty_df['incomes_normal'] - realty_df['expenses']
realty_df['profits_pessimistic'] = realty_df['incomes_pessimistic'] - realty_df['expenses']

realty_df_filtered = realty_df[(realty_df['floor'] == 1) &
                               (realty_df['area'] >= 40) &
                               (realty_df['price'] <= 190000) &
                               realty_df['commercial_type'].isin(['FREE_PURPOSE', 'RETAIL']) &
                               (realty_df['distance'] <= 6.7) &
                               (realty_df['already_taken'] == 0) &
                               (realty_df['competitors'] <= 1) &
                               (realty_df['profits_normal'] > 500000) &
                               (realty_df['profits_pessimistic'] > 0)]

print(realty_df_filtered)

