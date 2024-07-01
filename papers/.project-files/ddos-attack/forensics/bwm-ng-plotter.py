from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re

# Read the file
lines = Path('bwm_ng.log').read_text().splitlines()


def convert_units(val):
    if np.all(val < 1e3):
        return val, 'bits/s'
    elif np.all(val < 1e6):
        return val / 1e3, 'Kilobits/s'
    elif np.all(val < 1e9):
        return val / 1e6, 'Megabits/s'
    else:
        return val / 1e9, 'Gigabits/s'


# Prepare the data
data = []
for line in lines:
    if re.match(r'^\d+\.\d+,s\d+-eth\d+,', line):
        parts = line.strip().split(',')
        data.append({
            'timestamp': round(float(parts[0]), 2),
            'interface': parts[1],
            'bytes_out_s': float(parts[2]),
            'bytes_in_s': float(parts[3]),
            'bytes_total_s': float(parts[4]),
            'bytes_in': int(parts[5]),
            'bytes_out': int(parts[6]),
            "packets_out_s": float(parts[7]),
            "packets_in_s": float(parts[8]),
            "packets_total_s": float(parts[9]),
            "packets_in": int(parts[10]),
            "packets_out": int(parts[11]),
            "errors_out_s": float(parts[12]),
            "errors_in_s": float(parts[13]),
            "errors_in": int(parts[14]),
            "errors_out": int(parts[15]),
            "bits_out_s": float(parts[16]),
            "bits_in_s": float(parts[17]),
            "bits_total_s": float(parts[18]),
            "bits_in": int(parts[19]),
            "bits_out": int(parts[20])
        })

# Convert to DataFrame
df = pd.DataFrame(data)

# Get unique interfaces
interfaces = df['interface'].unique()

# Create subplots for each interface
fig, axs = plt.subplots(len(interfaces) + 2, 1, figsize=(10, 5 * len(interfaces)))

for i, interface in enumerate(interfaces):
    df_interface = df[df['interface'] == interface]
    y, unit = convert_units(df_interface['bytes_total_s'].values)
    axs[i].plot(df_interface['timestamp'], y, label=f'{interface} Total ({unit})')
    axs[i].set_title(f'Interface {interface}')
    axs[i].set_xlabel('Timestamp')
    axs[i].set_ylabel(unit)
    axs[i].legend()

df_filtered = df[df['interface'].isin(['s1-eth2', 's2-eth2', 's3-eth1'])]
df_sum = df_filtered.groupby('timestamp')['bytes_total_s'].sum().reset_index()
y, unit = convert_units(df_sum['bytes_total_s'].values)

df_s1_eth1 = df[df['interface'] == 's1-eth1']
y2, unit2 = convert_units(df_s1_eth1['bytes_total_s'].values)

# Create the plot
axs[-2].plot(df_sum['timestamp'], y, label=f'Sent Network Traffic ({unit})')
axs[-2].plot(df_s1_eth1['timestamp'], y2, label=f'Received Network Traffic ({unit2})')
axs[-2].set_title('Sent/Received Attack Network Traffic')
axs[-2].set_xlabel('Timestamp')
axs[-2].set_ylabel(unit)
axs[-2].legend()

# Create one big plot for all interfaces
for interface in interfaces:
    df_interface = df[df['interface'] == interface]
    y, unit = convert_units(df_interface['bytes_total_s'].values)
    axs[-1].plot(df_interface['timestamp'], y, label=f'{interface} Total ({unit})')
axs[-1].set_title('All Interfaces')
axs[-1].set_xlabel('Timestamp')
axs[-1].set_ylabel(unit)
axs[-1].legend()

plt.tight_layout()
plt.show()
