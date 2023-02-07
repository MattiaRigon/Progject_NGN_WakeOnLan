from scapy.all import *
import os

def packet_callback(packet):
    if packet[UDP].dport == 9:
        print("Magic packet detected!")
        os.system("lxterminal -e 'bash -c \"sudo python3 /home/pi/Desktop/next2022/server.py\"'")
            #lanci il server.py

print("Sniffing...")    
sniff(prn=packet_callback, filter="udp and broadcast", store=0)