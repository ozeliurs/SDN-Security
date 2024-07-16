# Forensics Directory

This directory contains Python scripts for analyzing and visualizing network traffic and bandwidth usage data generated during the DDoS attack demonstration. The scripts use data logged by `bwm-ng`, a console-based live network bandwidth monitor.

## Project Structure

The Forensics directory includes the following Python scripts:

- `bwm-ng-net-graph.py`: This script generates a network graph that visualizes the network traffic between different nodes in the network. The width of the edges in the graph represents the number of packets transmitted between the nodes.

- `bwm-ng-plotter.py`: This script generates plots for each network interface, showing the total bytes transmitted per second over time. It also generates a combined plot for all interfaces and a plot showing the sent and received network traffic during the attack.

## Usage

To use the scripts, navigate to the Forensics directory and execute the desired script:

```bash
cd forensics
python3 bwm-ng-net-graph.py
```

or

```bash
cd forensics
python3 bwm-ng-plotter.py
```

Please note that these scripts require the `bwm-ng.log` file generated during the DDoS attack demonstration. Make sure this file is located in the same directory as the scripts.

## Dependencies

The scripts in this directory require the following Python libraries:

- `pandas`
- `matplotlib`
- `numpy`
- `networkx`
- `imageio`
- `colour`

You can install these dependencies using pip:

```bash
pip install pandas matplotlib numpy networkx imageio colour
```

## Further Information

For a detailed explanation of the DDoS attack demonstration and the associated scripts, please refer to the main project README and the paper "Anatomy of a DDoS Attack: From Host Infection to Service Denial".