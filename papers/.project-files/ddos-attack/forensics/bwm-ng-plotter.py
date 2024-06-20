from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import re

# Read the file
lines = Path('bwm_ng.log').read_text().splitlines()

# Prepare the data
data = []
for line in lines:
    if re.match(r'^\d+\.\d+,s\d+-eth\d+,', line):
        parts = line.strip().split(',')
        data.append({
            'timestamp': float(parts[0]),
            'interface': parts[1],
            'bytes_out': float(parts[2]),
            'bytes_in': float(parts[3]),
            'bytes_total': float(parts[4])
        })

# Convert to DataFrame
df = pd.DataFrame(data)

# Get unique interfaces
interfaces = df['interface'].unique()

# Create subplots for each interface
fig, axs = plt.subplots(len(interfaces) + 1, 1, figsize=(10, 5 * len(interfaces)))

for i, interface in enumerate(interfaces):
    df_interface = df[df['interface'] == interface]
    axs[i].plot(df_interface['timestamp'], df_interface['bytes_total'], label=f'{interface} Bytes Total')
    axs[i].set_title(f'Interface {interface}')
    axs[i].set_xlabel('Timestamp')
    axs[i].set_ylabel('Bytes')
    axs[i].legend()

# Create one big plot for all interfaces
for interface in interfaces:
    df_interface = df[df['interface'] == interface]
    axs[-1].plot(df_interface['timestamp'], df_interface['bytes_total'], label=f'{interface} Bytes Total')
axs[-1].set_title('All Interfaces')
axs[-1].set_xlabel('Timestamp')
axs[-1].set_ylabel('Bytes')
axs[-1].legend()

plt.tight_layout()
plt.show()