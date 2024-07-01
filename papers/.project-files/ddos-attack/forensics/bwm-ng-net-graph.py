from pathlib import Path

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import re

# Read the file
lines = Path('bwm_ng.log').read_text().splitlines()

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

# Count the number of bytes in for each interface
bytes_in = df.groupby('interface')['bytes_in'].sum()

# Count the number of bytes out for each interface
bytes_out = df.groupby('interface')['bytes_out'].sum()

G = nx.DiGraph()

for node in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
    G.add_node(node)

for node in ['s1', 's2', 's3']:
    G.add_node(node)

G.add_weighted_edges_from([
    ('h1', 's1', bytes_in['s1-eth1']),
    ('s1', 'h1', bytes_out['s1-eth1']),
    ('h2', 's1', bytes_in['s1-eth2']),
    ('s1', 'h2', bytes_out['s1-eth2']),
    ('h3', 's2', bytes_in['s2-eth1']),
    ('s2', 'h3', bytes_out['s2-eth1']),
    ('h4', 's2', bytes_in['s2-eth2']),
    ('s2', 'h4', bytes_out['s2-eth2']),
    ('h5', 's3', bytes_in['s3-eth1']),
    ('s3', 'h5', bytes_out['s3-eth1']),
    ('h6', 's3', bytes_in['s3-eth2']),
    ('s3', 'h6', bytes_out['s3-eth2']),
    ('s1', 's2', bytes_in['s2-eth3']),
    ('s2', 's1', bytes_out['s1-eth3']),
    ('s2', 's3', bytes_in['s3-eth3']),
    ('s3', 's2', bytes_out['s2-eth4'])
])

print(G.edges(data=True))

# Draw the graph with width of the edges representing the number of packets
fig, ax = plt.subplots()
pos = nx.spring_layout(G, weight=None)
nx.draw_networkx_nodes(G, pos, ax=ax)
nx.draw_networkx_labels(G, pos, ax=ax)

edge_width = [np.log1p(G[u][v]['weight'])/4 for u, v in G.edges]
nx.draw_networkx_edges(G, pos, ax=ax, width=edge_width, connectionstyle='arc3,rad=0.1', edge_color='gray')
plt.show()