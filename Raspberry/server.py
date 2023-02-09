#!/usr/bin/env python

# -------------------------------------------------------------------
# Server.py - python script running in the Raspberry Pis that contains an HTTP Web Server answering HTTP GET/POST requests
# Allows to start and stop Docker containers sent by a client

from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json
import docker
from time import sleep
from termcolor import colored

MAX_RUNNING_CONTAINERS = 3
MAX_WEBAPPS = 3
ports = {}

# Ports structure to store the available ports

for i in range(1,MAX_WEBAPPS+1):
    ports[f"{i}"] = {
        "port": 8000+i,        # Port number
        "containerID": None,   # Container short ID
        "container": None      # Container number (1/2/3)
    }

# ----- TURN ON function ------

def turnOn(data, chosenPort=None): 
    client = docker.from_env()
    print(colored("----- Eseguo il container con image : docker" + data["DockerID"] + " -----", "green"))
    
    if int(data["DockerID"]) <= 3: # WEB-APP container
        container = client.containers.run("docker"+data["DockerID"], ports={80:chosenPort}, detach=True)
        for i in range(1,4):
            if ports[f"{i}"]["port"] == chosenPort:
                ports[f"{i}"]["containerID"] = container.short_id
                ports[f"{i}"]["container"] = data["DockerID"]
    else:
        container = client.containers.run("docker"+data["DockerID"], detach=True)

    ps = os.popen('docker ps -a').read()
    print(ps)       
    
# -----TURN OFF function ------

def turnOff(data):
    ps = os.popen('docker ps').read()
    if(data["DockerID"] not in ps):   # Container not running
        print(colored("----- Container non in esecuzione! Impossibile spegnerlo -----", "yellow"))
    else:
        client = docker.from_env() 
        container_list = client.containers.list()

        if data["port"] != None:   #PORT SPECIFIED
            ok = False
            for i in range(1,4):
                if ports[f"{i}"]["port"] == data["port"] and ports[f"{i}"]["container"] == data["DockerID"]:
                    cont = client.containers.get(ports[f"{i}"]["containerID"])
                    print(colored("----- Stoppo il container con image : docker" + data["DockerID"] + " sulla porta " + str(ports[f"{i}"]["port"]) + " -----", "green"))
                    cont.stop()
                    ports[f"{i}"]["container"] = None
                    ports[f"{i}"]["containerID"] = None
                    ok = True
                    break
            if(not ok):
                print(colored("******   ERRORE PORTA INSERITA  ******", "red"))   
        else:   # PORT NOT SPECIFIED
            for container in container_list:
                if("docker"+data["DockerID"]+":latest" == container.image.tags[0]):
                    cont = client.containers.get(container.short_id)
                    cont.stop()
            print(colored("----- Stoppo i container con image : docker" + data["DockerID"] + " -----", "green"))
            for i in range(1,4):
                if ports[f"{i}"]["container"] == data["DockerID"]:
                    ports[f"{i}"]["containerID"] = None
                    ports[f"{i}"]["container"] = None
        ps = os.popen('docker ps -a').read()
    print(ps)

    # Check if there are no containers running  -->  TURN OFF the server (SUICIDE)

    if int(os.popen('docker ps | grep Up | wc -l').read()) == 0: #turn off the server
        print(colored("Spegnimento del Server", "blue"))
        clDocker = "echo ''; echo '' ;echo 'Stopping...' ; docker stop $(docker ps --filter status=running -q) ; echo 'Removing...' ; docker rm $(docker ps --filter status=exited -q)"
        os.system(clDocker)
        exit(0)


class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        n = os.popen('docker ps | grep Up | wc -l').read()   #get the number of active containers 
        self.wfile.write(n.encode('utf-8'))  #send n
  
        return

    def do_POST(self):
        self.send_response(200)
        text = self.rfile.read(int(self.headers['Content-Length']))  # Retrieve the packet payload 
        self.end_headers()
        data = json.loads(text.decode('utf-8'))
        chosenPort = None

        if(data["action"] == "TurnOn"):
            if int(data["DockerID"]) <= 3:    # WEB-APP container  -> need to choose the port for the web-app
                for i in range(1,4):
                    if ports[f"{i}"]["containerID"] == None:
                        chosenPort = ports[f"{i}"]["port"]
                        break
                self.wfile.write(str(chosenPort).encode('utf-8'))     # Write the port in the HTTP response 
            else:
                self.wfile.write("".encode('utf-8')) 
            turnOn(data, chosenPort)
        
        elif(data["action"] == "TurnOff"):
            turnOff(data)

        elif(data["action"] == "print"):      # Answer the HTTP post with the running containers
            ps = os.popen('docker ps --format "table {{.Image}}SPACE{{.Status}}SPACE{{.Ports}}"').read()
            self.wfile.write(ps.encode('utf-8'))

        return

if __name__ == '__main__':
    server = HTTPServer(('', 8000), MyServer)
    print('Server in esecuzione...')
# Server start
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        clDocker = "echo ''; echo '' ;echo 'Stopping...' ; docker stop $(docker ps --filter status=running -q) ; echo 'Removing...' ; docker rm $(docker ps --filter status=exited -q)"
        os.system(clDocker)
        pass