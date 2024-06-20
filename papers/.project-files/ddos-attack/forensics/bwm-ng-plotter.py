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
fig, axs = plt.subplots(len(interfaces) + 1, 1, figsize=(10, 5 * len(interfaces)))

for i, interface in enumerate(interfaces):
    df_interface = df[df['interface'] == interface]
    axs[i].plot(df_interface['timestamp'], df_interface['bytes_total_s'], label=f'{interface} Bytes Total')
    axs[i].plot(df_interface['timestamp'], df_interface['errors_in'] + df_interface['errors_out'], color='red', label=f'{interface} Errors Total')
    axs[i].set_title(f'Interface {interface}')
    axs[i].set_xlabel('Timestamp')
    axs[i].set_ylabel('Bytes / Errors')
    axs[i].legend()

# Create one big plot for all interfaces
for interface in interfaces:
    df_interface = df[df['interface'] == interface]
    axs[-1].plot(df_interface['timestamp'], df_interface['bytes_total_s'], label=f'{interface} Bytes Total')
axs[-1].set_title('All Interfaces')
axs[-1].set_xlabel('Timestamp')
axs[-1].set_ylabel('Bytes')
axs[-1].legend()

plt.tight_layout()
plt.show()