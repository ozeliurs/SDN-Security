import re
from pathlib import Path

import imageio
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from tqdm import tqdm
from colour import Color

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

G = nx.DiGraph()

for node in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
    G.add_node(node)

for node in ['s1', 's2', 's3']:
    G.add_node(node)

G.add_weighted_edges_from([
    ('h1', 's1', 1),
    ('s1', 'h1', 1),
    ('h2', 's1', 1),
    ('s1', 'h2', 1),
    ('h3', 's2', 1),
    ('s2', 'h3', 1),
    ('h4', 's2', 1),
    ('s2', 'h4', 1),
    ('h5', 's3', 1),
    ('s3', 'h5', 1),
    ('h6', 's3', 1),
    ('s3', 'h6', 1),
    ('s1', 's2', 1),
    ('s2', 's1', 1),
    ('s2', 's3', 1),
    ('s3', 's2', 1)
])

# Draw the graph with width of the edges representing the number of packets
pos = nx.spring_layout(G, weight=None)

Path('tmp/*').unlink(missing_ok=True)
Path('tmp').mkdir(exist_ok=True)

colors = list(Color("green").range_to(Color("red"),101))

mini = min(df['bytes_in_s'].min(), df['bytes_out_s'].min())
maxi = max(df['bytes_in_s'].max(), df['bytes_out_s'].max())

for timestamp, df_group in tqdm(df.groupby('timestamp')):
    fig, ax = plt.subplots()
    ax.set_title(f'Timestamp: {timestamp}')
    nx.draw_networkx_nodes(G, pos, ax=ax)
    nx.draw_networkx_labels(G, pos, ax=ax)

    edges = [
        ('h1', 's1', df_group[(df_group['interface'] == 's1-eth1')]['bytes_in_s'].sum()),
        ('s1', 'h1', df_group[(df_group['interface'] == 's1-eth1')]['bytes_out_s'].sum()),
        ('h2', 's1', df_group[(df_group['interface'] == 's1-eth2')]['bytes_in_s'].sum()),
        ('s1', 'h2', df_group[(df_group['interface'] == 's1-eth2')]['bytes_out_s'].sum()),
        ('h3', 's2', df_group[(df_group['interface'] == 's2-eth1')]['bytes_in_s'].sum()),
        ('s2', 'h3', df_group[(df_group['interface'] == 's2-eth1')]['bytes_out_s'].sum()),
        ('h4', 's2', df_group[(df_group['interface'] == 's2-eth2')]['bytes_in_s'].sum()),
        ('s2', 'h4', df_group[(df_group['interface'] == 's2-eth2')]['bytes_out_s'].sum()),
        ('h5', 's3', df_group[(df_group['interface'] == 's3-eth1')]['bytes_in_s'].sum()),
        ('s3', 'h5', df_group[(df_group['interface'] == 's3-eth1')]['bytes_out_s'].sum()),
        ('h6', 's3', df_group[(df_group['interface'] == 's3-eth2')]['bytes_in_s'].sum()),
        ('s3', 'h6', df_group[(df_group['interface'] == 's3-eth2')]['bytes_out_s'].sum()),
        ('s1', 's2', df_group[(df_group['interface'] == 's1-eth3')]['bytes_out_s'].sum()),
        ('s2', 's1', df_group[(df_group['interface'] == 's1-eth3')]['bytes_in_s'].sum()),
        ('s2', 's3', df_group[(df_group['interface'] == 's2-eth4')]['bytes_out_s'].sum()),
        ('s3', 's2', df_group[(df_group['interface'] == 's2-eth4')]['bytes_in_s'].sum())
    ]

    edge_width = [np.log1p(edge[2]) / 4 for edge in edges]
    for i, edge in enumerate(edges):
        c = colors[int((edge[2] - mini) / (maxi - mini) * 100)]
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=[edge], width=edge_width[i], connectionstyle='arc3,rad=0.3', edge_color=c.hex)
    # nx.draw_networkx_edges(G, pos, ax=ax, width=edge_width, connectionstyle='arc3,rad=0.3', edge_color='gray')
    plt.savefig(f'tmp/{timestamp}.png')
    plt.close(fig)

images = []
for filename in sorted(Path('tmp').iterdir()):
    images.append(imageio.imread(filename))

Path('bwm_ng.gif').unlink(missing_ok=True)
imageio.mimsave('bwm_ng.gif', images, duration=0.5)