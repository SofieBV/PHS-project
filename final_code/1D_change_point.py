from fcts_data_formatting import day_to_month, day_to_quarter, import_datasets, time_interval, add_categories, \
                                HB_to_areas, extract_data, day_to_quarter, month_to_quarter
from fcts_change_point_detection import all_methods, pelt_search, binary_segm, change_finder, window_based, dynamic_program
import numpy as np

data31, data62, operations, diag, covid, beds, emerg = import_datasets(['31DayData', '62DayData', 'cancellations_by_board_november_2021', \
                                                         'diagnostics_by_board_september_2021', 'covid_2022', 'hospital_beds', \
                                                             'monthly_ae_waitingtimes_202111'])

covid_monthly = day_to_month(covid)
operations_monthly, diag_monthly, covid_monthly, emerg_monthly = HB_to_areas([operations, diag, covid_monthly, emerg],islist=True)

groupings = {'all_reg':['NCA','SCAN','WOSCAN']}
operations_monthly, diag_monthly, covid_monthly, emerg_monthly = add_categories([operations_monthly, diag_monthly, covid_monthly, \
                                                                                    emerg_monthly], groupings, islist=True)

for dataset in [operations_monthly, diag_monthly, covid_monthly, emerg_monthly]:
    print(dataset.index.names)
    dataset.info()

op_tot, op_can, op_cap = extract_data(operations_monthly, 'all_reg', 'HBT', ['TotalOperations', 'TotalCancelled', 'NonClinicalCapacityReason'])
di4, di6 = extract_data(diag_monthly, ('all_reg', 'Imaging','All Imaging'), ['HBT', 'DiagnosticTestType','DiagnosticTestDescription'], \
                                    ['NumberWaitingOverFourWeeks', 'NumberWaitingOverSixWeeks'])
de4, de6 = extract_data(diag_monthly, ('all_reg', 'Endoscopy','All Endoscopy'), ['HBT', 'DiagnosticTestType','DiagnosticTestDescription'], \
                                    ['NumberWaitingOverFourWeeks', 'NumberWaitingOverSixWeeks'])
cov_pos, cov_death = extract_data(covid_monthly, 'all_reg', 'HB', ['DailyPositive', 'DailyDeaths'])

datasets = [op_tot, op_can, di4, di6, de4, de6, cov_pos, cov_death]
names = ['Total_operations', 'Cancelled_operations', 'Diagnostic_imaging_4_weeks', 'Diagnostic_imaging_6_weeks', 'Diagnostic_endoscopy_4_weeks', \
            'Diagnostic_endoscopy_6_weeks', 'Positive_covid', 'Covid_deaths']

for i in range(len(names)):
    all_methods(datasets[i], names[i])

# for x in [op_tot, op_can, di4, di6, de4, de6, cov_pos, cov_death]:
#     change_finder(x)
#     pelt_search(x)
#     binary_segm(x)
#     window_based(x)
#     dynamic_program(x)