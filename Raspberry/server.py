#!/usr/bin/env python
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json
import docker
from time import sleep

def turnOn(data):

    ps = os.popen('docker ps').read()
    if(data["DockerID"] in ps):
        print("Container già in esecuzione ! ")
        print(ps)
    else:
        print("Eseguo il container con image : " + data["DockerID"])
        client = docker.from_env()
        #container = client.containers.run(data["DockerID"], "sleep infinity", detach=True)    
        #container = client.containers.run(data["DockerID"], "tail -f /dev/null", detach=True)     #docker run -d docker1 sh -c 'while sleep 3600; do :; done'
        container = client.containers.run(data["DockerID"], detach=True)
        ps = os.popen('docker ps -a').read()
        print(ps)
        
        
    

def turnOff(data):

    ps = os.popen('docker ps').read()
    if(data["DockerID"] not in ps):
        print("Container non in esecuzione ! Impossibile spegnerlo ")
        #print(ps)
    else:
        print("Stoppo il container con image : " + data["DockerID"])
        client = docker.from_env()
        container_list = client.containers.list()
        for container in container_list:
            if(data["DockerID"]+":latest" == container.image.tags[0]):
                cont = client.containers.get(container.short_id)
                cont.stop()
        ps = os.popen('docker ps -a').read()
    
    print(ps)


class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
    
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
        clDocker = "echo ''; echo '' ;echo 'Stopping...' ; docker stop $(docker ps --filter status=running -q) ; echo 'Removing...' ; docker rm $(docker ps --filter status=exited -q)"
        os.system(clDocker)
        pass