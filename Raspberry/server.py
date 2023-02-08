#!/usr/bin/env python
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json
import docker
from time import sleep
#from termcolor import colored

MAX_CONTAINERS = 3
ports = {}

for i in range(1,MAX_CONTAINERS+1):
    ports[f"{i}"] = {
        "port": 8000+i,
        "containerID": None,   #Short ID del container
        "container": None      #Numero del container (1/2/3)
    }

def turnOn(data, chosenPort):
    client = docker.from_env()
    print("----- Eseguo il container con image : docker" + data["DockerID"] + " -----")
    
    container = client.containers.run("docker"+data["DockerID"], ports={80:chosenPort}, detach=True)
    
    for i in range(1,4):
        if ports[f"{i}"]["port"] == chosenPort:
            ports[f"{i}"]["containerID"] = container.short_id
            ports[f"{i}"]["container"] = data["DockerID"]

    ps = os.popen('docker ps -a').read()
    print(ps)       
    

def turnOff(data):

    ps = os.popen('docker ps').read()
    if(data["DockerID"] not in ps):
        print("----- Container non in esecuzione! Impossibile spegnerlo -----")
    else:
        client = docker.from_env()
        container_list = client.containers.list()

        if data["port"] != None:   #PORT SPECIFIED
            for i in range(1,4):
                if ports[f"{i}"]["port"] == data["port"] and ports[f"{i}"]["container"] == data["DockerID"]:
                    cont = client.containers.get(ports[f"{i}"]["containerID"])
                    print("----- Stoppo il container con image : docker" + data["DockerID"] + " sulla porta " + str(ports[f"{i}"]["port"]) + " -----")
                    cont.stop()
                    ports[f"{i}"]["container"] = None
                    ports[f"{i}"]["containerID"] = None
                    break
            print("******   ERRORE PORTA INSERITA  ******")    #
        else:
            for container in container_list:
                if("docker"+data["DockerID"]+":latest" == container.image.tags[0]):
                    cont = client.containers.get(container.short_id)
                    print("----- Stoppo i container con image : docker" + data["DockerID"] + " -----")
                    cont.stop()
            for i in range(1,4):
                if ports[f"{i}"]["container"] == data["DockerID"]:
                    ports[f"{i}"]["containerID"] = None
                    ports[f"{i}"]["container"] = None
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
        self.end_headers()
        data = json.loads(text.decode('utf-8'))
        chosenPort = 0
        if(data["action"] == "TurnOn"):
            for i in range(1,4):
                if ports[f"{i}"]["containerID"] == None:
                    #ports[f"{i}"]["container"] = data["DockerID"]
                    chosenPort = ports[f"{i}"]["port"]
                    break
            turnOn(data, chosenPort)
            self.wfile.write(str(chosenPort).encode('utf-8'))     #get the number of docker 
        elif(data["action"] == "TurnOff"):
            turnOff(data)
        elif(data["action"] == "print"):
            ps = os.popen('docker ps -a').read()
            self.wfile.write(ps.encode('utf-8'))

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