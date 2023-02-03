#!/usr/bin/env python
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json
from time import sleep
from wakeonlan import send_magic_packet
import requests
       
MAX_CONTAINERS = 3
IPRPI1 = "192.168.43.176"
IPRPI2 = ""
MACRPI1 = "14.18.c3.58.9f.e4"
MACRPI2 = ""



class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
    
        return

    def do_POST(self):
        R1off = False
        R2off = False
        self.send_response(200)
        text = self.rfile.read(int(self.headers['Content-Length']))
        data = json.loads(text.decode('utf-8'))
        self.end_headers()

        try:
            r = requests.get(f'http://{IPRPI1}:8000')    #RASPBERRY 1
            print("RASP1")

            n1 = int(r.text)
            if n1<MAX_CONTAINERS:
                r = requests.post(f'http://{IPRPI1}:8000', json=data)

                self.wfile.write("Eseguo il docker sul Raspy 1".format(self.path).encode('utf-8'))
                return
            else:
                print("R1FULL")
        except:
            R1off = True
            print("R1OFF")
            pass
        
        try:
            r = requests.get(f'http://{IPRPI2}:8000')    #RASPBERRY 2
            n2 = int(r.text)
            if n2<MAX_CONTAINERS:
                r = requests.post(f'http://{IPRPI2}:8000', data=text)
                
                self.wfile.write("Eseguo il docker sul Raspy 2".format(self.path).encode('utf-8'))
                return

        except:
            #R2off = True
            print("R2OFF")
            pass

        if R1off:    #RPI1 OFF 
            send_magic_packet(MACRPI1)
            sleep(5)
            r = requests.post(f'http://{IPRASP1}:8000', data=text)
            
            self.wfile.write("Eseguo il docker sul Raspy 1".format(self.path).encode('utf-8'))
        elif R2off:    #RPI2 OFF
            send_magic_packet(MACRPI2)
            sleep(5)
            r = requests.post(f'http://{IPRPI2}:8000', data=text)
            
            self.wfile.write("Eseguo il docker sul Raspy 2".format(self.path).encode('utf-8'))
        else:           #BOTH FULL
            print("SEGMENTATION FAULT")

            self.wfile.write("Segmentation Fault".format(self.path).encode('utf-8'))

    

        # os.path.dirname(os.path.abspath(__file__))
        # esecuzione = os.popen('./wakeon.sh {0}'.format(text.decode('utf-8'))).read()
        # print(esecuzione)
        return

if __name__ == '__main__':
# Creiamo un oggetto HTTPServer che ascolterà sulla porta 8000
    server = HTTPServer(('', 8000), MyServer)
    print('Server in esecuzione...')
# Avvio server
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass