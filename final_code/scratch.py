from data_formatting import import_datasets, time_interval, add_categories, HB_to_areas

data31, data62 = import_datasets(['31DayData', '62DayData'])
data31 = time_interval(data31, ['2018Q1', '2020Q1'])
data31 = HB_to_areas(data31)

groupings = {'new_CT':['Breast', 'Cervical'], 'all_reg':['NCA','SCAN','WOSCAN']}
data31 = add_categories(data31, groupings)

print(data31.xs(('all_reg', 'all_reg','new_CT'),level=['HB', 'HBT','CancerType']))

data31, data62, referrals = import_datasets(['31DayData', '62DayData','cancellations_by_board_november_2021'])
referrals = time_interval(referrals, [201807, 202107])
referrals = HB_to_areas(referrals)

print(referrals.xs('NCA',level='HBT')['TotalOperations'])