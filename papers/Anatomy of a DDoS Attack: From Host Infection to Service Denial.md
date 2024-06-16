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

## Monitoring Tools

To monitor and analyze the network traffic and performance, we use `bwm-ng` (Bandwidth Monitor NG) to monitor the throughput on network interfaces. This helps us understand the volume of traffic generated during the attack.

We also use `tcpdump` to capture and analyze packets on the network. It provides detailed insights into the nature of the traffic and helps in understanding the attack patterns and the commands between compromised hosts and the command and control server.

# Host Compromise

# Launching the Attack

# Demo

# Forensics

# Conclusion and Mitigation

# Sources