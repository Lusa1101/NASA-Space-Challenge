import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Function to calculate STA/LTA ratio
def sta_lta_algorithm(data, sta_window, lta_window, threshold):
    """
    data: Pandas DataFrame containing time and velocity data
    sta_window: window size for short-term average
    lta_window: window size for long-term average
    threshold: STA/LTA ratio threshold for moonquake detection
    """
    # Initialize arrays for STA, LTA, and the ratio
    sta = np.zeros(len(data))
    lta = np.zeros(len(data))
    sta_lta_ratio = np.zeros(len(data))
    
    # Loop through data to calculate STA, LTA, and the ratio
    for i in range(lta_window, len(data)):
        # Calculate STA (short-term average)
        sta[i] = np.mean(data['velocity'][i-sta_window:i])
        
        # Calculate LTA (long-term average)
        lta[i] = np.mean(data['velocity'][i-lta_window:i])
        
        # Avoid division by zero in the LTA calculation
        if lta[i] != 0:
            sta_lta_ratio[i] = sta[i] / lta[i]
        else:
            sta_lta_ratio[i] = 0
    
    # Identify points where STA/LTA exceeds the threshold
    moonquake_indices = np.where(sta_lta_ratio < threshold)[0]
    
    return moonquake_indices, sta_lta_ratio

# Example: Read data from CSV (replace with your actual CSV file)
df = pd.read_csv(r'./first.csv')

# STA/LTA algorithm parameters
sta_window = 50 
lta_window = 500  
threshold = 10.0  # Threshold for STA/LTA ratio to detect moonquake

# Apply STA/LTA algorithm to detect moonquakes
moonquake_indices, sta_lta_ratio = sta_lta_algorithm(df, sta_window, lta_window, threshold)
number_of_moonquakes = len(moonquake_indices)

# Plot the STA/LTA ratio and detected moonquakes
plt.figure(figsize=(12, 6))
plt.plot(df['time_rel'], sta_lta_ratio, label="STA/LTA Ratio", color='blue')
plt.axhline(y=threshold, color='red', linestyle='--', label="Threshold")
plt.scatter(df['time_rel'][moonquake_indices], sta_lta_ratio[moonquake_indices], color='green', label="Detected Moonquakes", zorder=3)
plt.title("STA/LTA Moonquake Detection")
plt.xlabel("Relative Time (sec)")
plt.ylabel("STA/LTA Ratio")
plt.legend()
plt.show()

# Output the indices of detected moonquakes
print(f"Detected moonquakes at indices: {moonquake_indices}")
print(number_of_moonquakes)