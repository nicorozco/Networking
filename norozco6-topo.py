#!/usr/bin/python
# Nicolas Orozco | CSE-150 | Python Topology
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink

class MyTopology(Topo):
    """
    A basic topology
    """
    def __init__(self):
        Topo.__init__(self)

        # Set Up Topology Here
        s1 = self.addSwitch('Switch1') ## Add Switch 1
        s2 = self.addSwitch('Switch2') ## Add Switch 2

        h1 = self.addHost('Desktop',ip = '10.1.1.1')   ## Adds a Host
        h2 = self.addHost('Laptop', ip = '10.1.1.2')
        
        h3 = self.addHost('Lights', ip = '10.1.2.1')
        h4 = self.addHost('Fridge', ip = '10.1.2.2')
        
        # Add Links
        self.addLink(s1,h1)
        self.addLink(s1,h2)

        # Add Links
        self.addLink(s2,h3)
        self.addLink(s2,h4)
        self.addLink(s1,s2)


if __name__ == '__main__':
    """
    If this script is run as an executable (by chmod +x), this is
    what it will do
    """
    topo = MyTopology()                   ## Creates the topology
    net = Mininet(topo=topo, link=TCLink) ## Loads the topology
    net.start()                           ## Starts Mininet

    # Commands here will run on the simulated topology
    CLI(net)
