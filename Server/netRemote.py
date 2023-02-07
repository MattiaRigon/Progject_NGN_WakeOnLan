#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.cli import CLI
from mininet.link import Intf
from mininet.log import setLogLevel, info


def myNetwork():

    net = Mininet( topo=None,
                   build=False)

    info( '*** Adding controller\n' )
    net.addController(name='c0', controller=RemoteController)
    info( '*** Add switches\n')
    s1 = net.addSwitch('s1')
    Intf( 'eth1', node=s1 )

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', ip='0.0.0.0', mac='aa:bb:cc:dd:ee:01') #DHCP 
    
    info( '*** Add links\n')
    net.addLink(h1, s1)
    #net.addLink(h2, s1)

    info( '*** Starting network\n')
    net.start()
    h1.cmdPrint('dhclient '+h1.defaultIntf().name) #DHCP
    
    h1.cmd('sudo python3 hostServer.py &')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()