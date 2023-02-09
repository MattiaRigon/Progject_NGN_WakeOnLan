from scapy.all import *
import os

def packet_callback(packet):
    if packet[UDP].dport == 9:  # one raspberry port 9 , the other one port 10
        print("Magic packet detected!")
        os.system("lxterminal -e 'sudo python3 /home/pi/Desktop/next2022/server.py'")
            #lanci il server.py

print("Sniffing...")    
sniff(prn=packet_callback, filter="udp and broadcast", store=0)