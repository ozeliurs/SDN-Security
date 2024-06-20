# DDoS Attack Demonstration Project

This project contains the source code and related files for the paper "Anatomy of a DDoS Attack: From Host Infection to Service Denial". It demonstrates a Distributed Denial of Service (DDoS) attack in a controlled environment using Mininet for network emulation.

## Project Structure

The project is organized into several subdirectories, each containing different components of the DDoS attack demonstration:

- [`lab`](https://github.com/ozeliurs/SDN-Security/tree/main/papers/.project-files/ddos-attack/lab): This directory contains the Python scripts that set up the network environment and launch the DDoS attack. The `main.py` script is the main entry point for the demonstration.

- [`php-exploit`](https://github.com/ozeliurs/SDN-Security/tree/main/papers/.project-files/ddos-attack/php-exploit): This directory contains PHP scripts demonstrating a file upload vulnerability. It includes both the vulnerable version of the script (`vuln-webserver.php`) and a patched version that mitigates the vulnerability (`patched-webserver.php`).

- [`virus`](https://github.com/ozeliurs/SDN-Security/tree/main/papers/.project-files/ddos-attack/virus): This directory contains a Python script that simulates a simple virus. The virus connects to a command and control server to receive and execute commands.

- [`ssh-bruteforce`](https://github.com/ozeliurs/SDN-Security/tree/main/papers/.project-files/ddos-attack/ssh-bruteforce): This directory contains a Python script that demonstrates a brute force attack on an SSH server using a list of common passwords.

- [`forensics`](https://github.com/ozeliurs/SDN-Security/tree/main/papers/.project-files/ddos-attack/forensics): This directory contains tools and scripts for analyzing network traffic and bandwidth usage during and after the DDoS attack.

## Usage

To run the DDoS attack demonstration, navigate to the `lab` directory and execute the `main.py` script:

```bash
cd lab
python3 main.py
```

Please note that this script should be run in an isolated environment, as it involves creating a network and launching a DDoS attack. It is intended for educational purposes only.

## Further Reading

For a detailed explanation of the DDoS attack demonstration and the associated scripts, please refer to the paper "Anatomy of a DDoS Attack: From Host Infection to Service Denial", available [here](https://github.com/ozeliurs/SDN-Security/tree/main/papers/Anatomy%20of%20a%20DDoS%20Attack%3A%20From%20Host%20Infection%20to%20Service%20Denial.md).