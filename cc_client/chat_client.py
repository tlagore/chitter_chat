import socket
import threading

class ChatClient:
    """Chat server class to handle chat server interactions"""

    def __init__(self, host, port):
        """constructor for chat client"""
        print("{0} {1}".format(host, port))
        
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((host, port))

        listenServer = threading.Thread(target=self.listen_server)
        listenClient = threading.Thread(target=self.listen_client)

        listenServer.start()
        listenClient.start()

    def listen_server(self):
        """listens for interaction from the server""" 
        print("Listening server")
        
    def listen_client(self):
        """listen for client input to pass to the server"""
        print("Listening client")
        
    def __del__(self):
        """destructor for chat client"""
