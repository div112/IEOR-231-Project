import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df_single_city = pd.read_csv('single_city_MC_data.csv', delimiter=',')

df_single_city['naive_cost_perkWh_Commuters'] = df_single_city['total_Commuter_naive_cost'] / df_single_city['total_Commuter_naive_energy_charged']
df_single_city['naive_cost_perkWh_Ubers'] = df_single_city['total_Uber_naive_cost'] / df_single_city['total_Uber_naive_energy_charged']

df_single_city['scheduled_cost_perkWh_Commuters'] = df_single_city['total_Commuter_scheduled_cost'] / df_single_city['total_Commuter_scheduled_energy_charged']
df_single_city['scheduled_cost_perkWh_Ubers'] = df_single_city['total_Uber_scheduled_cost'] / df_single_city['total_Uber_scheduled_energy_charged']

fig, axs = plt.subplots(1, 2, figsize=(12, 5))
df_single_city[['naive_cost_perkWh_Commuters', 'scheduled_cost_perkWh_Commuters']].hist(bins=20, ax=axs)
axs[0].set_title('Mean Cost of Naive Charging per kWh for Commuters')
axs[0].set_xlabel('Cost [$/kWh]')
axs[0].set_ylabel('Frequency')
axs[0].set_xlim(0, 0.26)
axs[1].set_title('Mean Cost of Scheduled Charging per kWh for Commuters')
axs[1].set_xlabel('Cost [$/kWh]')
axs[1].set_ylabel('Frequency')
axs[1].set_xlim(0, 0.26)
plt.savefig('single_city_commuter_cost_per_kWh.png', dpi = 300)

plt.show()

fig, axs = plt.subplots(1, 2, figsize=(12, 5))
df_single_city[['naive_cost_perkWh_Ubers', 'scheduled_cost_perkWh_Ubers']].hist(bins=20, ax=axs)
axs[0].set_title('Mean Cost of Naive Charging per kWh for Uber drivers')
axs[0].set_xlabel('Cost [$/kWh]')
axs[0].set_ylabel('Frequency')
axs[0].set_xlim(0, 0.26)
axs[1].set_title('Mean Cost of Scheduled Charging per kWh for Uber drivers')
axs[1].set_xlabel('Cost [$/kWh]')
axs[1].set_ylabel('Frequency')
axs[1].set_xlim(0, 0.26)
plt.savefig('single_city_uber_cost_per_kWh.png', dpi = 300)
plt.show()



df_single_city['naive_plugged_time_perkWh_Commuters'] = df_single_city['total_Commuter_naive_time_plugged_in'] / df_single_city['total_Commuter_naive_energy_charged']
df_single_city['naive_plugged_time_perkWh_Ubers'] = df_single_city['total_Uber_naive_time_plugged_in'] / df_single_city['total_Uber_naive_energy_charged']

df_single_city['scheduled_plugged_time_perkWh_Commuters'] = df_single_city['total_Commuter_scheduled_time_plugged_in'] / df_single_city['total_Commuter_scheduled_energy_charged']
df_single_city['scheduled_plugged_time_perkWh_Ubers'] = df_single_city['total_Uber_scheduled_time_plugged_in'] / df_single_city['total_Uber_scheduled_energy_charged']

# Histogram of the time plugged in
fig, axs = plt.subplots(1, 2, figsize=(14, 5))
df_single_city[['naive_plugged_time_perkWh_Commuters', 'scheduled_plugged_time_perkWh_Commuters']].hist(bins=20, ax=axs)
axs[0].set_title('Plugged-in time of Naive Charging per kWh for Commuters')
axs[0].set_xlabel('minutes/kWh')
axs[0].set_ylabel('Frequency')
#axs[0].set_xlim(0.06, 0.26)
axs[1].set_title('Plugged-in time of Scheduled Charging per kWh for Commuters')
axs[1].set_xlabel('minutes/kWh')
axs[1].set_ylabel('Frequency')
#axs[1].set_xlim(0.06, 0.26)
plt.savefig('single_city_commuter_plugged_time_per_kWh.png', dpi = 300)
plt.show()


fig, axs = plt.subplots(1, 2, figsize=(14, 5))
df_single_city[['naive_plugged_time_perkWh_Ubers', 'scheduled_plugged_time_perkWh_Ubers']].hist(bins=20, ax=axs)
axs[0].set_title('Plugged-in time of Naive Charging per kWh for Uber drivers')
axs[0].set_xlabel('minutes/kWh')
axs[0].set_ylabel('Frequency')
#axs[0].set_xlim(0, 0.2)
axs[1].set_title('Plugged-in timeof Scheduled Charging per kWh for Uber drivers')
axs[1].set_xlabel('minutes/kWh')
axs[1].set_ylabel('Frequency')
#axs[1].set_xlim(0, 0.2)
plt.savefig('single_city_uber_plugged_time_per_kWh.png', dpi = 300)
plt.show()





#### We plot the same histograms except for the case where we have 
#### create a new city for each simulation
df_multiple_cities = pd.read_csv('multiple_cities_MC_data.csv', delimiter=',')

df_multiple_cities['naive_cost_perkWh_Commuters'] = df_multiple_cities['total_Commuter_naive_cost'] / df_multiple_cities['total_Commuter_naive_energy_charged']
df_multiple_cities['naive_cost_perkWh_Ubers'] = df_multiple_cities['total_Uber_naive_cost'] / df_multiple_cities['total_Uber_naive_energy_charged']

df_multiple_cities['scheduled_cost_perkWh_Commuters'] = df_multiple_cities['total_Commuter_scheduled_cost'] / df_multiple_cities['total_Commuter_scheduled_energy_charged']
df_multiple_cities['scheduled_cost_perkWh_Ubers'] = df_multiple_cities['total_Uber_scheduled_cost'] / df_multiple_cities['total_Uber_scheduled_energy_charged']

fig, axs = plt.subplots(1, 2, figsize=(12, 5))
df_multiple_cities[['naive_cost_perkWh_Commuters', 'scheduled_cost_perkWh_Commuters']].hist(bins=20, ax=axs)
axs[0].set_title('Mean Cost of Naive Charging per kWh for Commuters')
axs[0].set_xlabel('Cost [$/kWh]')
axs[0].set_ylabel('Frequency')
axs[0].set_xlim(0.08, 0.26)
axs[1].set_title('Mean Cost of Scheduled Charging per kWh for Commuters')
axs[1].set_xlabel('Cost [$/kWh]')
axs[1].set_ylabel('Frequency')
axs[1].set_xlim(0.08, 0.26)
plt.savefig('multiple_cities_commuter_cost_per_kWh.png', dpi = 300)
plt.show()

fig, axs = plt.subplots(1, 2, figsize=(12, 5))
df_multiple_cities[['naive_cost_perkWh_Ubers', 'scheduled_cost_perkWh_Ubers']].hist(bins=20, ax=axs)
axs[0].set_title('Mean Cost of Naive Charging per kWh for Uber drivers')
axs[0].set_xlabel('Cost [$/kWh]')
axs[0].set_ylabel('Frequency')
axs[0].set_xlim(0, 0.18)
axs[1].set_title('Mean Cost of Scheduled Charging per kWh for Uber drivers')
axs[1].set_xlabel('Cost [$/kWh]')
axs[1].set_ylabel('Frequency')
axs[1].set_xlim(0, 0.18)
plt.savefig('multiple_cities_uber_cost_per_kWh.png', dpi = 300)
plt.show()



df_multiple_cities['naive_plugged_time_perkWh_Commuters'] = df_multiple_cities['total_Commuter_naive_time_plugged_in'] / df_multiple_cities['total_Commuter_naive_energy_charged']
df_multiple_cities['naive_plugged_time_perkWh_Ubers'] = df_multiple_cities['total_Uber_naive_time_plugged_in'] / df_multiple_cities['total_Uber_naive_energy_charged']

df_multiple_cities['scheduled_plugged_time_perkWh_Commuters'] = df_multiple_cities['total_Commuter_scheduled_time_plugged_in'] / df_multiple_cities['total_Commuter_scheduled_energy_charged']
df_multiple_cities['scheduled_plugged_time_perkWh_Ubers'] = df_multiple_cities['total_Uber_scheduled_time_plugged_in'] / df_multiple_cities['total_Uber_scheduled_energy_charged']

# Histogram of the time plugged in
fig, axs = plt.subplots(1, 2, figsize=(14, 5))
df_multiple_cities[['naive_plugged_time_perkWh_Commuters', 'scheduled_plugged_time_perkWh_Commuters']].hist(bins=20, ax=axs)
axs[0].set_title('Plugged-in time of Naive Charging per kWh for Commuters')
axs[0].set_xlabel('minutes/kWh')
axs[0].set_ylabel('Frequency')
#axs[0].set_xlim(0.06, 0.26)
axs[1].set_title('Plugged-in time of Scheduled Charging per kWh for Commuters')
axs[1].set_xlabel('minutes/kWh')
axs[1].set_ylabel('Frequency')
#axs[1].set_xlim(0.06, 0.26)
plt.savefig('multiple_cities_commuter_plugged_time_per_kWh.png', dpi = 300)
plt.show()

fig, axs = plt.subplots(1, 2, figsize=(14, 5))
df_multiple_cities[['naive_plugged_time_perkWh_Ubers', 'scheduled_plugged_time_perkWh_Ubers']].hist(bins=20, ax=axs)
axs[0].set_title('Plugged-in time of Naive Charging per kWh for Uber drivers')
axs[0].set_xlabel('minutes/kWh')
axs[0].set_ylabel('Frequency')
#axs[0].set_xlim(0, 0.2)
axs[1].set_title('Plugged-in timeof Scheduled Charging per kWh for Uber drivers')
axs[1].set_xlabel('minutes/kWh')
axs[1].set_ylabel('Frequency')
#axs[1].set_xlim(0, 0.2)
plt.savefig('multiple_cities_uber_plugged_time_per_kWh.png', dpi = 300)
plt.show()