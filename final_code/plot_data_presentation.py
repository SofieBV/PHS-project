from fcts_data_formatting import day_to_month, day_to_quarter, import_datasets, time_interval, add_categories, \
                                HB_to_areas, extract_data, day_to_quarter, month_to_quarter
import numpy as np
import matplotlib.pyplot as plt
from fcts_change_point_detection import all_methods, pelt_search, binary_segm, change_finder, window_based, dynamic_program

data31, covid = import_datasets(['31DayDataUpdate','covid_2022'])
covid = day_to_quarter(covid)
data31, covid = time_interval([data31, covid], ['2015Q2', '2021Q3'], islist=True)
data31, covid = HB_to_areas([data31, covid],islist=True)
groupings = {'all_reg':['NCA','SCAN','WOSCAN']}
data31, covid = add_categories([data31, covid], groupings, islist=True)

for dataset in [data31,covid]:
    print(dataset.index.names)
    dataset.info()

fig, ax = plt.subplots(2, 1, figsize=(16, 8), constrained_layout=True)
fig.patch.set_alpha(0)

plt.rcParams['font.size']='20'
plt.rcParams['xtick.color'] = '1'
plt.rcParams['ytick.color'] = '1'
plt.rcParams['legend.frameon'] = 'False'

ax = ax.ravel()

r31, t31 = extract_data(data31, ('all_reg', 'all_reg','All Cancer Types'), ['HB', 'HBT','CancerType'], \
                                        ['NumberOfEligibleReferrals31DayStandard', 'NumberOfEligibleReferralsTreatedWithin31Days'])
cov_pos, cov_death = extract_data(covid, 'all_reg', 'HB', ['DailyPositive', 'DailyDeaths'])

add = np.concatenate(([r31[0,:-int(len(cov_pos[0,:]))]], [np.zeros(len(r31[0,:])-len(cov_pos[0,:]))]), axis=0)
cov_pos = np.concatenate((add, cov_pos), axis=1)
cov_death = np.concatenate((add, cov_death), axis=1)

ax[0].set_title('Cancer waiting times 31 day standard', size=28, color='1')
ax[0].plot(r31[0,:],r31[1,:], label='31 day referrals in scotland',linewidth=4, color=(55/255,163/255,120/255))
ax[0].plot(t31[0,:],t31[1,:], label='31 day treated in scotland',linewidth=4, color=(164/255,42/255,148/255))
ax[0].set_ylabel('Nr of patients', size=24, color='1')
ax[1].set_title('Quarterly covid data', size=28, color='1')
ax[1].plot(cov_death[0,:],cov_death[1,:], label='covid deaths in scotland',linewidth=4, color=(55/255,163/255,120/255))
ax[1].set_xlabel('Quarters', size=24, color='1')
ax[1].set_ylabel('Nr of covid deaths', size=24, color='1')

for i in range(len(ax)):
    ax[i].tick_params(axis='x',labelrotation=45, colors='1', labelsize=20)
    ax[i].tick_params(axis='y', colors='1', labelsize=20)
    ax[i].set_facecolor('1')
    ax[i].legend()

ax[0].xaxis.set_ticklabels([])
every_nth = 1
for n, label in enumerate(ax[1].xaxis.get_ticklabels()):
    if n % every_nth != 0:
        label.set_visible(False)
plt.savefig('results/data31_covid_presentation.png')
plt.show()

