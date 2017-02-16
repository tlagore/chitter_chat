import threading
import socket
import re

class ChatServer:
    """Chat server class to handle chat server interactions"""
    # continue
    def __init__(self, port):
        """ChatServer Constructor"""
        self._port = port
        self._chat_groups = {}
        self._connected_clients = {}
        self._socket = 0

    def start_server(self):
        """Initializes the server socket"""
        ip = socket.gethostbyname(socket.getfqdn())
        print("Starting server on port {0}".format(self._port))
        print("Please ensure port forwarding for {0} on port {1}".format(ip, self._port))

        if re.match("127.0.*", ip):
            print("If this number is 127.0.0.1 or similar, comment out")
            print("{0}\t{1}".format(ip, socket.getfqdn()))
            print("in /etc/hosts")

        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            #self._socket.bind((socket.gethostname(), self._port))
            self._socket.bind(('127.0.0.1', self._port))
            self._listen()
        except socket.error as ex:
            print("Error initializing socket: {0}".format(type(ex).__name__))
            
            
    def _listen(self):
        """Listen for a client"""
        self._socket.listen(1);
        (client, address) = self._socket.accept()
        clientThread = threading.Thread(target=self._worker, args=((client, address),))
        clientThread.start()
        
        
    def _worker(self, args):
        """Handle a client"""
        print("working!")

    def __del__(self):
        try:
            self._socket.close()
        except:
            print("Error closing socket. May not have been initialized")
        finally:
            print("Server exitting.")

class Client:
    """Representation of a client"""
    def __init__(self):
        """Client Constructor"""

class ChatGroup:
    """Representation of a chat group"""
