 # Import libraries
import numpy as np
import pandas as pd
from obspy import read
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import functions


d1 = pd.read_csv(r'C:\Users\omphu\Documents\Hackathon\NASAHackathon\space_apps_2024_seismic_detection\data\lunar\training\data\S12_GradeA\first.csv')
d2 = pd.read_csv(r'C:\Users\omphu\Documents\Hackathon\NASAHackathon\space_apps_2024_seismic_detection\data\lunar\test\data\S12_GradeB\xa.s12.00.mhz.1977-07-19HR00_evid00991.csv')
d3 = pd.read_csv(r'C:\Users\omphu\Documents\Hackathon\NASAHackathon\space_apps_2024_seismic_detection\data\lunar\training\catalogs\apollo12_catalog_GradeA_final.csv')
d4 = pd.read_csv(r'C:\Users\omphu\Documents\Hackathon\NASAHackathon\space_apps_2024_seismic_detection\data\mars\test\data\XB.ELYSE.02.BHV.2019-05-23HR02_evid0041.csv')
mars_data = pd.read_csv(r'C:\Users\omphu\Documents\Hackathon\NASAHackathon\space_apps_2024_seismic_detection\data\mars\training\data\XB.ELYSE.02.BHV.2022-01-02HR04_evid0006.csv')

import numpy as np

print(mars_data.dtypes)

print(d1.dtypes)

# Assuming 'velocity' is a Pandas Series or NumPy array of the noise data
noise_mean = np.mean(d1['velocity(m/s)'].to_list())  # Use a period known to contain only noise
noise_std = np.std(d1['velocity(m/s)'].to_list())

# Set the threshold at 3 standard deviations above the mean
threshold = noise_mean + 3 * noise_std


d1 = functions.good_data(d4, 'velocity(m/s)')

#d1.to_csv('new_data.csv')

row = d1.iloc[6]
arrival_time = datetime.strptime(row['time_abs(%Y-%m-%dT%H:%M:%S.%f)'],'%Y-%m-%dT%H:%M:%S.%f')
arrival_time_rel = row['time_rel']

# Read in time steps and velocities
csv_times = np.array(d1['time_rel(sec)'].tolist())
csv_data = np.array(d1['velocity(m/s)'].tolist())

# Plot the trace! 
fig,ax = plt.subplots(1,1,figsize=(10,3))
ax.plot(csv_times,csv_data)

# Make the plot pretty
ax.set_xlim([min(csv_times),max(csv_times)])
ax.set_ylabel('Velocity (m/s)')
ax.set_xlabel('Time (s)')
ax.set_title('Mars Original Data', fontweight='bold')

# Plot where the arrival time is
arrival_line = ax.axvline(x=arrival_time_rel, c='red', label='Rel. Arrival')
ax.legend(handles=[arrival_line])
plt.show()

