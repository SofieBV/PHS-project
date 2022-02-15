from fcts_data_formatting import day_to_month, day_to_quarter, import_datasets, time_interval, add_categories, \
                                HB_to_areas, extract_data, day_to_quarter, month_to_quarter
import numpy as np
import matplotlib.pyplot as plt

data31, data62, cancer = import_datasets(['31DayDataUpdate', '62DayDataUpdate', 'cancerdata_fixed_sofie'])
cancer = cancer.groupby(cancer.index.names).sum()
cancer = month_to_quarter(cancer)

data31, data62, cancer = time_interval([data31, data62, cancer], ['2019Q1', '2021Q2'], islist=True)
data31, data62, cancer = HB_to_areas([data31, data62, cancer],islist=True)

for dataset in [data31, data62, cancer]:
    print(dataset.index.names)
    dataset.info()


fig, ax = plt.subplots(2, 2, figsize=(16, 8), constrained_layout=True)
ax = ax.ravel()

i=0
for area in ['NCA', 'SCAN', 'WOSCAN']:
    r31, t31 = extract_data(data31, (area, area,'All Cancer Types'), ['HB', 'HBT','CancerType'], \
                                            ['NumberOfEligibleReferrals31DayStandard', 'NumberOfEligibleReferralsTreatedWithin31Days'])
    r62, t62 = extract_data(data62, (area, area,'All Cancer Types'), ['HB', 'HBT','CancerType'], \
                                            ['NumberOfEligibleReferrals62DayStandard', 'NumberOfEligibleReferralsTreatedWithin62Days'])
    can = extract_data(cancer, (area, 'All Cancers', 'All', 'All Ages'), ['HB', 'CancerType', 'Sex', 'Age Group'], ['Count'])

    ax[i].set_title('Cancer in {}'.format(area))
    ax[i].plot(r31[0,:],r31[1,:], label='31 day referrals')
    ax[i].plot(t31[0,:],t31[1,:], label='31 day treated')
    ax[i].plot(can[0,:], can[1,:], label='cancer diagnosis')
    ax[i].plot(r62[0,:],r62[1,:], label='62 day referrals')
    ax[i].plot(r62[0,:],r62[1,:], label='62 day referrals')

    ax[i].legend()
    ax[i].tick_params('x',labelrotation=45)
    every_nth = 1
    for n, label in enumerate(ax[i].xaxis.get_ticklabels()):
        if n % every_nth != 0:
            label.set_visible(False)

    i +=1

groupings = {'all_reg':['NCA','SCAN','WOSCAN']}
data31, data62, cancer = add_categories([data31, data62, cancer], groupings, islist=True)

r31, t31 = extract_data(data31, ('all_reg', 'all_reg','All Cancer Types'), ['HB', 'HBT','CancerType'], \
                                            ['NumberOfEligibleReferrals31DayStandard', 'NumberOfEligibleReferralsTreatedWithin31Days'])
r62, t62 = extract_data(data62, ('all_reg', 'all_reg','All Cancer Types'), ['HB', 'HBT','CancerType'], \
                                        ['NumberOfEligibleReferrals62DayStandard', 'NumberOfEligibleReferralsTreatedWithin62Days'])
can = extract_data(cancer, ('all_reg', 'All Cancers', 'All', 'All Ages'), ['HB', 'CancerType', 'Sex', 'Age Group'], ['Count'])

ax[3].set_title('Cancer in {}'.format('all regions'))
ax[3].plot(r31[0,:],r31[1,:], label='31 day referrals')
ax[3].plot(t31[0,:],t31[1,:], label='31 day treated')
ax[3].plot(can[0,:], can[1,:], label='cancer diagnosis')
ax[3].plot(r62[0,:],r62[1,:], label='62 day referrals')
ax[3].plot(r62[0,:],r62[1,:], label='62 day referrals')

ax[3].legend()
ax[3].tick_params('x',labelrotation=45)
every_nth = 1
for n, label in enumerate(ax[3].xaxis.get_ticklabels()):
    if n % every_nth != 0:
        label.set_visible(False)

plt.savefig('results/compare_cancer_data2.png')
plt.show()