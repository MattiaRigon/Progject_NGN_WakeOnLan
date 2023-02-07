#!/usr/bin/env python
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json
import docker
from time import sleep

def turnOn(data):

    ps = os.popen('docker ps').read()
    if(data["DockerID"] in ps):
        print("----- Container già in esecuzione! -----")
        print(ps)
    else:
        print("----- Eseguo il container con image : docker" + data["DockerID"] + " -----")
        client = docker.from_env()
        porta = "800"+data["DockerID"]
        container = client.containers.run("docker"+data["DockerID"], ports={80:int(porta)}, detach=True)
        ps = os.popen('docker ps -a').read()
        print(ps)        
    

def turnOff(data):

    ps = os.popen('docker ps').read()
    if(data["DockerID"] not in ps):
        print("----- Container non in esecuzione! Impossibile spegnerlo -----")
    else:
        print("----- Stoppo il container con image : docker" + data["DockerID"] + " -----")
        client = docker.from_env()
        container_list = client.containers.list()
        for container in container_list:
            if("docker"+data["DockerID"]+":latest" == container.image.tags[0]):
                cont = client.containers.get(container.short_id)
                cont.stop()
        ps = os.popen('docker ps -a').read()    
    print(ps)


class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        n = os.popen('docker ps | grep Up | wc -l').read()   #get the number of active containers 
        self.wfile.write(n.encode('utf-8'))  #send n
  
        return

    def do_POST(self):
        self.send_response(200)
        text = self.rfile.read(int(self.headers['Content-Length']))
        data = json.loads(text.decode('utf-8'))
        if(data["action"] == "TurnOn"):
            turnOn(data)
        elif(data["action"] == "TurnOff"):
            turnOff(data)
        self.end_headers()

        return

if __name__ == '__main__':
    server = HTTPServer(('', 8000), MyServer)
    print('Server in esecuzione...')
    # Avvio server
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        clDocker = "echo ''; echo '' ;echo 'Stopping...' ; docker stop $(docker ps --filter status=running -q) ; echo 'Removing...' ; docker rm $(docker ps --filter status=exited -q)"
        os.system(clDocker)
        pass