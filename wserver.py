import threading
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer
import json
WS_PORT = '8091'

clients = []
servers = []

properties = {}

class Handler(WebSocket):
    def handleMessage(self):
        print('Got message: ' + self.data)
        if self.data == 'status':
            self.sendMessage(json.dumps(properties))
            servers.append(self)
        else:
            obj = json.loads(self.data)
            if 'action' in obj:
                properties[obj['action']] = obj['num']
            for client in clients:
                if client != self:
                    if client in servers:
                        self.sendMessage(json.dumps(properties))
                    else:
                        client.sendMessage(self.data)

    def handleConnected(self):
        print('Connected:' + str(self), end='')
        #clients.sendMessage(json.dumps(properties))
        print(':> ' + json.dumps(properties))
        clients.append(self)

    def handleClose(self):
        print('Closed:' + str(self))
        clients.remove(self)



def serve():
    server = SimpleWebSocketServer('0.0.0.0', WS_PORT, Handler)

    print("Starting websocket..." + WS_PORT)
    while True:
        server.serveforever()


def serve_threaded():
    t = threading.Thread(target=serve)
    t.start()

serve_threaded()
