import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler



def load_data(file_path):
    data = np.loadtxt(file_path)
    return data
    

def good_data(data, variable):
    threshold = get_threshold(data, variable)
    data1 = data[abs(data[f'{variable}']) >= threshold]
    #data1 = data1[['time_rel(sec)', f'{variable}']]
    return data1


def bad_data(data, variable):
    threshold = get_threshold(data, variable)
    data1 = data[abs(data[f'{variable}']) < threshold]
    data1 = data1[['time_rel(sec)', f'{variable}']]
    return data1


def group_data(data, column, value):
    return data[data[f'{column}'] == value]


def get_list_files():
    path = r'C:\Users\omphu\Documents\Hackathon\NASAHackathon\space_apps_2024_seismic_detection\data\lunar\training\catalogs\apollo12_catalog_GradeA_final.csv'
    files = pd.read_csv(path)
    return files['filename'].to_list()


def bring_data_together(data_path, data):
    df = pd.read_csv(data_path)
    folders = ['impact_mq', 'deep_mq', 'shallow_mq']
    for folder in folders:
        df = group_data(df, 'mq_type', f'{folder}')
        data = group_data(data, 'mq_type', f'{folder}')
        frames = [data, df]
        frames = pd.concat(frames)
        frames.to_csv(f'{folder}/combined_data.csv', index=True)



def linking_files():
    files = get_list_files()
    data = pd.read_csv('first.csv')
    for file in files:
        if(os.path.splitext(f'{file}')[0] == 'xa'):       #pathlib.Path(f'{file}').suffix == '.csv'):
            bring_data_together(f'{file}.csv', data)



def group_data(data, column, value):
    return data[data[f'{column}'] == value]


def rename_col(data, old_col, new_col):
    d1 = data.rename(columns={
            f'{old_col}': f'{new_col}'
        }, inplace=True)
    return d1


def get_threshold(data, variable):
    noise_mean = np.mean(data[f'{variable}'].to_list())
    noise_std = np.std(data[f'{variable}'].to_list())
    threshold = noise_mean + 4 * noise_std
    return threshold


def make_plot(d1, variable):
    row = d1.iloc[6]
    arrival_time = datetime.strptime(row['time_abs(%Y-%m-%dT%H:%M:%S.%f)'],'%Y-%m-%dT%H:%M:%S.%f')
    arrival_time_rel = row['time_rel(sec)']

    # Read in time steps and velocities
    csv_times = np.array(d1['time_rel(sec)'].tolist())
    csv_data = np.array(d1[variable].tolist())

    # Plot the trace! 
    fig,ax = plt.subplots(1,1,figsize=(10,3))
    ax.plot(csv_times,csv_data)

    # Make the plot pretty
    ax.set_xlim([min(csv_times),max(csv_times)])
    ax.set_ylabel(variable)
    ax.set_xlabel('Time (s)')
    ax.set_title('Testing 1', fontweight='bold')

    # Plot where the arrival time is
    arrival_line = ax.axvline(x=arrival_time_rel, c='red', label='Rel. Arrival')
    ax.legend(handles=[arrival_line])
    #plt.show()
    
    return ax




