#!/usr/bin/env python
import argparse
import sys
import socket
import random
import struct

import time
from threading import Thread

from scapy.all import sendp, send, get_if_list, get_if_hwaddr
from scapy.all import Packet
from scapy.all import Ether, IP, UDP, TCP

def get_if():
    ifs=get_if_list()
    iface=None # "h1-eth0"
    for i in get_if_list():
        if "eth0" in i:
            iface=i
            break;
    if not iface:
        print "Cannot find eth0 interface"
        exit(1)
    return iface

def packet_send(address, iface, payload):
	pkt =  Ether(src=get_if_hwaddr(iface), dst='ff:ff:ff:ff:ff:ff')
	#pkt = pkt /IP(dst=addr) / TCP(dport=1234, sport=random.randint(49152,65535)) / sys.argv[2]
	pkt = pkt /IP(dst=address) / TCP(dport=1234, sport=27777) / payload
	pkt.show2()
	for i in range(1000):
		sendp(pkt, iface=iface, verbose=False)
		
def main():

	if len(sys.argv)<3:
		print 'pass 2 arguments: <destination> "<message>"'
		exit(1)

	addr = socket.gethostbyname(sys.argv[1])
	iface = get_if()

	print "sending on interface %s to %s" % (iface, str(addr))
	
	threadpool = 100
	thread = []
	for i in range(threadpool):
		thread.append(Thread(target=packet_send, args=(addr, iface, sys.argv[2])))
		thread[i].start()
		
	for i in range(threadpool):
		thread[i].join()


if __name__ == '__main__':
    main()
