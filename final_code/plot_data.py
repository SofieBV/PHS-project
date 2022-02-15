from fcts_data_formatting import day_to_month, day_to_quarter, import_datasets, time_interval, add_categories, \
                                HB_to_areas, extract_data, day_to_quarter, month_to_quarter
import numpy as np
import matplotlib.pyplot as plt

data31, data62, operations, diag, covid, beds, emerg = import_datasets(['31DayDataUpdate', '62DayDataUpdate', 'cancellations_by_board_november_2021', \
                                                         'diagnostics_by_board_september_2021', 'covid_2022', 'hospital_beds', \
                                                             'monthly_ae_waitingtimes_202111'])

covid_monthly = day_to_month(covid)
operations_monthly, diag_monthly, covid_monthly, emerg_monthly = time_interval([operations, diag, covid_monthly, emerg], \
                                                                         ['201505', '202109'], islist=True)
operations_monthly, diag_monthly, covid_monthly, emerg_monthly = HB_to_areas([operations_monthly, diag_monthly, covid_monthly, \
                                                                                        emerg_monthly],islist=True)

for dataset in [operations_monthly, diag_monthly, covid_monthly, emerg_monthly]:
    print(dataset.index.names)
    dataset.info()

fig, ax = plt.subplots(3, 2, figsize=(16, 16), constrained_layout=True)
ax = ax.ravel()

for area in ['NCA', 'SCAN', 'WOSCAN']:
    op_tot, op_can, op_cap = extract_data(operations_monthly, area, 'HBT', ['TotalOperations', 'TotalCancelled', 'NonClinicalCapacityReason'])
    di4, di6 = extract_data(diag_monthly, (area, 'Imaging','All Imaging'), ['HBT', 'DiagnosticTestType','DiagnosticTestDescription'], \
                                        ['NumberWaitingOverFourWeeks', 'NumberWaitingOverSixWeeks'])
    de4, de6 = extract_data(diag_monthly, (area, 'Endoscopy','All Endoscopy'), ['HBT', 'DiagnosticTestType','DiagnosticTestDescription'], \
                                        ['NumberWaitingOverFourWeeks', 'NumberWaitingOverSixWeeks'])
    cov_pos, cov_death = extract_data(covid_monthly, area, 'HB', ['DailyPositive', 'DailyDeaths'])

    add = np.concatenate(([op_tot[0,:-int(len(cov_pos[0,:]))]], [np.zeros(len(op_tot[0,:])-len(cov_pos[0,:]))]), axis=0)
    cov_pos = np.concatenate((add, cov_pos), axis=1)
    cov_death = np.concatenate((add, cov_death), axis=1)

    ax[0].set_title('Operations cancelled')
    ax[0].plot(op_tot[0,:],op_can[1,:]/op_tot[1,:], label='perc oper cancelled in {}'.format(area))
    ax[1].set_title('Operations cancelled')
    ax[1].plot(op_tot[0,:],op_tot[1,:], label='total operations planned in {}'.format(area))
    ax[2].set_title('Diagnostic waiting times over 4 weeks')
    ax[2].plot(di4[0,:],di4[1,:], label='imaging 4 weeks in {}'.format(area))
    ax[2].plot(de4[0,:],de4[1,:], label='endoscopy 4 weeks in {}'.format(area))
    ax[3].set_title('Diagnostic waiting times over 6 weeks')
    ax[3].plot(di6[0,:],di6[1,:], label='imaging 6 weeks in {}'.format(area))
    ax[3].plot(de6[0,:],de6[1,:], label='endoscopy 6 weeks in {}'.format(area))
    ax[4].set_title('Quarterly covid data')
    ax[4].plot(cov_pos[0,:],cov_pos[1,:], label='positive covid in {}'.format(area))
    ax[5].set_title('Quarterly covid data')
    ax[5].plot(cov_death[0,:],cov_death[1,:], label='covid deaths in {}'.format(area))
    
    for i in range(len(ax)):
        ax[i].legend()
        ax[i].tick_params('x',labelrotation=45)
        every_nth = 2
        for n, label in enumerate(ax[i].xaxis.get_ticklabels()):
            if n % every_nth != 0:
                label.set_visible(False)
plt.savefig('results/some_datasets_plotted_monthly.png')
plt.show()

## now plot things quarterly
covid = day_to_quarter(covid)
operations, diag, emerg = month_to_quarter([operations, diag, emerg], islist=True)
data31, data62, operations, diag, covid, beds, emerg = time_interval([data31, data62, operations, diag, covid, beds, emerg], \
                                                                         ['2015Q2', '2021Q3'], islist=True)
data31, data62, operations, diag, covid, beds, emerg = HB_to_areas([data31, data62, operations, diag, covid, beds, emerg],islist=True)

for dataset in [data31, data62, operations, diag, covid, beds, emerg]:
    print(dataset.index.names)
    dataset.info()


fig, ax = plt.subplots(4, 2, figsize=(32, 16), constrained_layout=True)
ax = ax.ravel()

for area in ['NCA', 'SCAN', 'WOSCAN']:
    r31, t31 = extract_data(data31, (area, area,'All Cancer Types'), ['HB', 'HBT','CancerType'], \
                                            ['NumberOfEligibleReferrals31DayStandard', 'NumberOfEligibleReferralsTreatedWithin31Days'])
    r62, t62 = extract_data(data62, (area, area,'All Cancer Types'), ['HB', 'HBT','CancerType'], \
                                            ['NumberOfEligibleReferrals62DayStandard', 'NumberOfEligibleReferralsTreatedWithin62Days'])
    op_tot, op_can, op_cap = extract_data(operations, area, 'HBT', ['TotalOperations', 'TotalCancelled', 'NonClinicalCapacityReason'])
    di4, di6 = extract_data(diag, (area, 'Imaging','All Imaging'), ['HBT', 'DiagnosticTestType','DiagnosticTestDescription'], \
                                        ['NumberWaitingOverFourWeeks', 'NumberWaitingOverSixWeeks'])
    de4, de6 = extract_data(diag, (area, 'Endoscopy','All Endoscopy'), ['HBT', 'DiagnosticTestType','DiagnosticTestDescription'], \
                                        ['NumberWaitingOverFourWeeks', 'NumberWaitingOverSixWeeks'])
    cov_pos, cov_death = extract_data(covid, area, 'HB', ['DailyPositive', 'DailyDeaths'])

    add = np.concatenate(([r31[0,:-int(len(cov_pos[0,:]))]], [np.zeros(len(r31[0,:])-len(cov_pos[0,:]))]), axis=0)
    cov_pos = np.concatenate((add, cov_pos), axis=1)
    cov_death = np.concatenate((add, cov_death), axis=1)

    ax[0].set_title('Cancer waiting times 31 day standard')
    ax[0].plot(r31[0,:],r31[1,:], label='31 day referrals in {}'.format(area))
    ax[0].plot(t31[0,:],t31[1,:], label='31 day treated in {}'.format(area))
    ax[1].set_title('Cancer waiting times 62 day standard')
    ax[1].plot(r62[0,:],r62[1,:], label='62 day referrals in {}'.format(area))
    ax[1].plot(r62[0,:],r62[1,:], label='62 day referrals in {}'.format(area))
    ax[2].set_title('Operations cancelled')
    ax[2].plot(op_tot[0,:],op_can[1,:]/op_tot[1,:], label='perc oper cancelled in {}'.format(area))
    ax[3].set_title('Operations cancelled')
    ax[3].plot(op_tot[0,:],op_tot[1,:], label='total operations planned in {}'.format(area))
    ax[4].set_title('Diagnostic waiting times over 4 weeks')
    ax[4].plot(di4[0,:],di4[1,:], label='imaging 4 weeks in {}'.format(area))
    ax[4].plot(de4[0,:],de4[1,:], label='endoscopy 4 weeks in {}'.format(area))
    ax[5].set_title('Diagnostic waiting times over 6 weeks')
    ax[5].plot(di6[0,:],di6[1,:], label='imaging 6 weeks in {}'.format(area))
    ax[5].plot(de6[0,:],de6[1,:], label='endoscopy 6 weeks in {}'.format(area))
    ax[6].set_title('Quarterly covid data')
    ax[6].plot(cov_pos[0,:],cov_pos[1,:], label='positive covid in {}'.format(area))
    ax[7].set_title('Quarterly covid data')
    ax[7].plot(cov_death[0,:],cov_death[1,:], label='covid deaths in {}'.format(area))
    
    for i in range(len(ax)):
        ax[i].legend()
        ax[i].tick_params('x',labelrotation=45)
        every_nth = 1
        for n, label in enumerate(ax[i].xaxis.get_ticklabels()):
            if n % every_nth != 0:
                label.set_visible(False)
plt.savefig('results/some_datasets_plotted_quarterly.png')
plt.show()