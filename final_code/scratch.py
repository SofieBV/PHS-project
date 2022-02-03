from data_formatting import day_to_month, day_to_quarter, import_datasets, time_interval, add_categories, \
                                HB_to_areas, extract_data, day_to_quarter, month_to_quarter
import numpy as np
import matplotlib.pyplot as plt

data31, data62, operations, diag, covid = import_datasets(['31DayData', '62DayData', 'cancellations_by_board_november_2021', \
                                                         'diagnostics_by_board_september_2021', 'covid_2022'])
print(covid)
data31 = time_interval(data31, ['2018Q1', '2020Q1'])
data31 = HB_to_areas(data31)

groupings = {'new_CT':['Breast', 'Cervical'], 'all_reg':['NCA','SCAN','WOSCAN']}
data31 = add_categories(data31, groupings)
print(data31.index.names)
data31.info()

d31 = extract_data(data31, ('all_reg', 'all_reg','new_CT'), ['HB', 'HBT','CancerType'], ['NumberOfEligibleReferrals31DayStandard'])

covid = day_to_quarter(covid)
print(covid)

operations = time_interval(operations, [201807, 202107])
operations = HB_to_areas(operations)
print(operations.index.names)
operations.info()

op1, op2 = extract_data(operations, 'NCA', 'HBT', ['TotalOperations', 'TotalCancelled'])

fig, ax = plt.subplots(1, 1, figsize=(8, 4))
ax.plot(op1[0,:],op1[1,:])
every_nth = 4
for n, label in enumerate(ax.xaxis.get_ticklabels()):
    if n % every_nth != 0:
        label.set_visible(False)
plt.show()