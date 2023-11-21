#!/usr/bin/env python
from subprocess import call

from mininet.cli import CLI
from mininet.link import Intf
from mininet.link import TCLink
from mininet.log import info
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.node import Controller
from mininet.node import CPULimitedHost
from mininet.node import Host
from mininet.node import IVSSwitch
from mininet.node import Node
from mininet.node import OVSController
from mininet.node import OVSKernelSwitch
from mininet.node import RemoteController
from mininet.node import UserSwitch


def myNetwork():
    """ """
    net = Mininet(topo=None, build=False, ipBase="10.0.0.0/8")

    info("*** Adding controller\n")
    c0 = net.addController(name="c0", controller=Controller, protocol="tcp", port=6633)

    info("*** Add switches\n")
    s1 = net.addSwitch("s1", cls=OVSKernelSwitch)

    info("*** Add hosts\n")
    h3 = net.addHost("h3", cls=Host, ip="10.0.0.3", defaultRoute=None)
    h2 = net.addHost("h2", cls=Host, ip="10.0.0.2", defaultRoute=None)
    h1 = net.addHost("h1", cls=Host, ip="10.0.0.1", defaultRoute=None)
    h5 = net.addHost("internet", cls=Host, ip="10.0.0.101", defaultRoute=None)
    h4 = net.addHost("h4", cls=Host, ip="10.0.0.4", defaultRoute=None)

    info("*** Add links\n")
    net.addLink(h1, s1, bw=1)
    net.addLink(h2, s1, bw=1)
    net.addLink(h3, s1, bw=1)
    net.addLink(h4, s1, bw=1)
    net.addLink(h5, s1)

    info("*** Starting HTTP server on every host\n")
    h1.cmd("cd ~/proj/Draft/Server && python3 -m http.server 80 &")
    h2.cmd("cd ~/proj/Draft/Server && python3 -m http.server 80 &")
    h3.cmd("cd ~/proj/Draft/Server && python3 -m http.server 80 &")

    info("*** Starting network\n")
    net.build()
    info("*** Starting controllers\n")
    for controller in net.controllers:
        controller.start()

    info("*** Starting switches\n")
    net.get("s1").start([c0])

    info("*** Post configure switches and hosts\n")

    CLI(net)
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    myNetwork()
