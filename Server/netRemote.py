#!/usr/bin/python

# netRemote.py - python script that creates the Mininet virtual network
# One host h1 used for the web server that routes the requests traffic, the virtual switch s1 is linked with the interface eth1 to allow the 
# communication with the real network

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.cli import CLI
from mininet.link import Intf
from mininet.log import setLogLevel, info
import subprocess


def myNetwork():

    net = Mininet( topo=None,
                   build=False)

    info( '*** Adding controller\n' )
    net.addController(name='c0', controller=RemoteController)

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1')
    Intf( 'eth1', node=s1 )   #Add interface eth1 to switch s1 to allow connection with real network

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', ip='0.0.0.0', mac='aa:bb:cc:dd:ee:01') #DHCP 
    #h1 = net.addHost('h1', ip='192.168.43.119', mac='aa:bb:cc:dd:ee:01')   #STATIC

    info( '*** Add links\n')
    net.addLink(h1, s1)

    info( '*** Starting network\n')
    net.start()
    h1.cmdPrint('dhclient '+h1.defaultIntf().name) #DHCP
    
    h1.cmd('sudo python3 hostServer.py &')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()