"""
iperf.py: Run iperf between all hosts in a Mininet topology.
The aim is to test multiple architectures and controllers.
"""
import time

from pprint import pprint

from mininet.net import Mininet
from mininet.node import OVSKernelSwitch
from mininet.topo import MinimalTopo
from mininet.log import setLogLevel
from mininet.clean import Cleanup

setLogLevel('info')

data = {}

def collect_data(net, label):
    global data

    net.start()
    try:
        data[label] = net.iperf()
    finally:
        net.stop()
        Cleanup.cleanup()

def main():
    collect_data(
        Mininet(topo=MinimalTopo(), switch=OVSKernelSwitch),
        'ovs_kernel_switch'
    )

    pprint(data)


if __name__ == '__main__':
    main()