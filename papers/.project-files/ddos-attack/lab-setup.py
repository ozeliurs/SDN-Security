from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel


def create_network():
    # Create a network
    net = Mininet(controller=Controller, link=TCLink, switch=OVSSwitch)

    # Add a controller
    net.addController('c0')

    # Add switches
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')

    # Add hosts and links to s1
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    net.addLink(h1, s1, bw=200)
    net.addLink(h2, s1, bw=100)

    # Add hosts and links to s2
    h3 = net.addHost('h3')
    h4 = net.addHost('h4')
    net.addLink(h3, s2, bw=100)
    net.addLink(h4, s2, bw=100)

    # Add hosts and links to s3
    h5 = net.addHost('h5')
    h6 = net.addHost('h6')
    net.addLink(h5, s3, bw=100)
    net.addLink(h6, s3, bw=100)

    # Add links between switches
    net.addLink(s1, s2, bw=1000)
    net.addLink(s2, s3, bw=1000)

    # Start the network
    net.start()

    # Install docker on h2
    h2.cmd('curl -fsSL https://get.docker.com | sh')
    # Install DVWA on h2
    h2.cmd('wget https://raw.githubusercontent.com/digininja/DVWA/master/compose.yml')
    h2.cmd('docker-compose -f compose.yml up -d')

    # Enable SSH on h5
    h5.cmd('apt-get update')
    h5.cmd('apt-get install -y openssh-server')
    # Set a weak password for root (toor)
    h5.cmd('echo "root:toor" | chpasswd')


if __name__ == '__main__':
    setLogLevel('info')
    create_network()