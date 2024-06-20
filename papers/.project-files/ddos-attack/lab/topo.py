class DDOSTopo():
    @staticmethod
    def build(net):
        # Add a controller
        net.addController('c0')
        
        # Add switches
        s1 = net.addSwitch('s1')
        s2 = net.addSwitch('s2')
        s3 = net.addSwitch('s3')
        
        # Add hosts
        h1 = net.addHost('h1', ip='10.42.0.1')
        h2 = net.addHost('h2', ip='10.42.0.2')
        h3 = net.addHost('h3', ip='10.42.0.3')
        h4 = net.addHost('h4', ip='10.42.0.4')
        h5 = net.addHost('h5', ip='10.42.0.5')
        h6 = net.addHost('h6', ip='10.42.0.6')

        # Add links
        net.addLink(h1, s1, bw=200)
        net.addLink(h2, s1, bw=100)
        net.addLink(h3, s2, bw=100)
        net.addLink(h4, s2, bw=100)
        net.addLink(h5, s3, bw=100)
        net.addLink(h6, s3, bw=100)

        net.addLink(s1, s2, bw=1000)
        net.addLink(s2, s3, bw=1000)

