import threading
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer

WS_PORT = '8091'

clients = []


class Handler(WebSocket):
    def handleMessage(self):
        print('Got message: ' + self.data)
        for client in clients:
            if client != self:
                client.sendMessage(self.data)

    def handleConnected(self):
        print('Connected:' + str(self))
        clients.append(self)

    def handleClose(self):
        print('Closed:' + str(self))
        clients.remove(self)



def serve():
    server = SimpleWebSocketServer('0.0.0.0', WS_PORT, Handler)

    print("Starting websocket..." + WS_PORT)
    while True:
        try:
            server.serveforever()
        except Exception as exc:
            print(str(exc))
            pass


def serve_threaded():
    t = threading.Thread(target=serve)
    t.start()

serve_threaded()