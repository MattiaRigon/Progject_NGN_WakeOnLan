#!/usr/bin/env python

# hostServer.py - python script running on h1 virtual host. It contains an HTTP Server Web to receive the client requests and route them 
# to the correct servers (Raspberry Pis), based on their actual state

from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json
from time import sleep
from wakeonlan import send_magic_packet
import requests
       
MAX_CONTAINERS = 3
RPI1 = "rpi1.ngn-project.com"          #192.168.43.188
MACRPI1 = "b8:27:eb:2d:cb:df"

RPI2 = "rpi2.ngn-project.com"          #192.168.43.147
MACRPI2 = "b8:27:eb:0d:0a:72"



class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        print("GET")
    
        return

    def do_POST(self):
        R1off = False
        R2off = False
        self.send_response(200)
        
        #Read the POST message
        textByte = self.rfile.read(int(self.headers['Content-Length']))
        dataJson = json.loads(textByte.decode('utf-8'))
        
        self.end_headers()

        #Check the 'action' value of the data sent in the packet

        #----TURN OFF-----
        if dataJson["action"] == "TurnOff":
            if dataJson["RaspberryIP"] != None:    #specific RASPBERRY  -> POST to that Rpi
                try:
                    r = requests.post(f'http://{dataJson["RaspberryIP"]}:8000', data=textByte)
                    self.wfile.write("Turn Off ".format(self.path).encode('utf-8'))
                except:
                    pass                
                return

            else:   #RASPBERRY not specified -> POST to both Rpi
                try:
                    r1 = requests.post(f'http://{RPI1}:8000', data=textByte)
                except:
                    pass
                try:
                    r2 = requests.post(f'http://{RPI2}:8000', data=textByte)
                except:
                    pass
                self.wfile.write("Turn Off ".format(self.path).encode('utf-8'))
                return

        #----PRINT-----
        #POST to both the RPis to know their current state     

        elif dataJson["action"] == "print":
                r1 = ""
                r2 = ""
                try:
                    r1 = requests.post(f'http://{RPI1}:8000', data=textByte)
                except:
                    pass
                try:
                    r2 = requests.post(f'http://{RPI2}:8000', data=textByte)
                except:
                    pass
                if (r1 == ""):
                    if r2 == "":
                        resp = " \n\n "
                    else:
                        resp = f" \n\n{r2.text}"
                else:
                    if r2 == "":
                        resp = f"{r1.text}\n\n "
                    else:
                        resp = f"{r1.text}\n\n{r2.text}"
                self.wfile.write(resp.encode('utf-8'))
                return
        
        #----TURN ON----
        
        try:   
            r = requests.get(f'http://{RPI1}:8000')    #GET to RASPBERRY 1 to verify if it is ON and to know his current state            
            n1 = int(r.text)
            if n1<MAX_CONTAINERS:  # IF Rpi 1 has free space             
                r = requests.post(f'http://{RPI1}:8000', data=textByte)
                self.wfile.write(f"Eseguo il container {dataJson['DockerID']} sul Raspy 1 ({RPI1}) sulla porta {r.text}".format(self.path).encode('utf-8'))
                return
        except:
            R1off = True    #RASPBERRY 1 is OFF
            pass
        
        try:
            r = requests.get(f'http://{RPI2}:8000')    #GET to RASPBERRY 2 to verify if it is ON and to know his current state
            n2 = int(r.text)
            if n2<MAX_CONTAINERS:
                r = requests.post(f'http://{RPI2}:8000', data=textByte)

                self.wfile.write(f"Eseguo il container sul Raspy 2 ({RPI2}) sulla porta {r.text}".format(self.path).encode('utf-8'))
                return

        except:
            R2off = True    #RASPBERRY 2 is OFF
            pass

        if R1off:    #RPI1 OFF 
            send_magic_packet(MACRPI1, port=10)  #Wake On LAN Rpi 1
            sleep(5)   #Wait 5 seconds to lets the server start

            r = requests.post(f'http://{RPI1}:8000', data=textByte)     #POST to Rpi 1
            self.wfile.write(f"Eseguo il container sul Raspy 1 ({RPI1}) sulla porta {r.text}".format(self.path).encode('utf-8'))
        elif R2off:    #RPI2 OFF
            send_magic_packet(MACRPI2, port=9)   #Wake On LAN Rpi 1
            sleep(5)   #Wait 5 seconds to lets the server start

            r = requests.post(f'http://{RPI2}:8000', data=textByte)     #POST ro Rpi 2
            self.wfile.write(f"Eseguo il container sul Raspy 2 ({RPI2}) sulla porta {r.text}".format(self.path).encode('utf-8'))
        else:           #BOTH FULL
            print("SEGMENTATION FAULT")
            self.wfile.write("Segmentation Fault (spazio nei server non disponibile, riprova più tardi...)".format(self.path).encode('utf-8'))
        return

if __name__ == '__main__':
# Create an HTTPServer Object listening to port 8000 
    server = HTTPServer(('', 8000), MyServer)
    print('Server in esecuzione...')
# Start server
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass