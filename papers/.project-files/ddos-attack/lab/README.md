# DDoS Attack Demonstration Lab

This project contains a set of Python scripts that set up a network environment using Mininet to demonstrate a Distributed Denial of Service (DDoS) attack.

## Files

### main.py

This is the main script that sets up the network, infects hosts, and launches the DDoS attack. It uses the Mininet library to create a network with a specific topology, infects certain hosts with a simple virus, and then uses these infected hosts to launch a DDoS attack on a target host.

The script also includes functionality for monitoring network traffic during the attack, capturing packets for analysis, and logging the results.

### topo.py

This script defines the network topology for the DDoS attack demonstration. It uses the Mininet library to create a network with a specific number of hosts and switches, and to define the links between them.

## How it works

1. The `main.py` script first sets up the network using the topology defined in `topo.py`.
2. It then infects certain hosts with a simple virus that connects to a command and control server to receive commands.
3. Once the hosts are infected, the script launches a DDoS attack on a target host.
4. During the attack, the script monitors network traffic and captures packets for analysis.
5. After the attack, the script logs the results and cleans up the network.

## Usage

To run the DDoS attack demonstration, execute the `main.py` script:

```bash
python3 main.py
```

Please note that this script should be run in an isolated environment, as it involves creating a network and launching a DDoS attack. It is intended for educational purposes only.