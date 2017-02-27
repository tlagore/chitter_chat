import json
import hashlib
import pickle
import random
import re
import socket
import threading
import traceback
import sys

from message import Message

class ChatServer:
    """Chat server class to handle chat server interactions"""
    # continue
    def __init__(self, port):
        """ChatServer Constructor"""
        self._port = port
        self._chat_groups = {}
        self._connected_clients = {}
        self._socket = 0
        self._users = {}
        try:
            with open('u.txt') as inFile:
                self._users = json.load(inFile)
        except:
            print("Error loading users, file might not exist")

    def start_server(self):
        """Initializes the server socket"""
        ip = socket.gethostbyname(socket.getfqdn())
        print("Starting server on port {0}".format(self._port))
        print("Please ensure port forwarding for {0} on port {1}".format(ip, self._port))

        if re.match("127.0.*", ip):
            print("If this number is 127.0.0.1 or similar, comment out")
            print("{0}\t{1}".format(ip, socket.getfqdn()))
            print("In /etc/hosts")

        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            #TODO change this to the host name when you figure this out
            #self._socket.bind(("0.0.0.0", self._port))
            self._socket.bind(('127.0.0.1', self._port))
            self._listen()
        except socket.error as ex:
            print("Error initializing socket: {0}".format(type(ex).__name__))
            
    def _listen(self):
        """Listen for a client"""
        while True:
            self._socket.listen(5);
            (client, address) = self._socket.accept()
            print("Client connected.")
            clientThread = threading.Thread(target=self._worker, args=((client, address),))
            clientThread.start()            
    
    def _worker(self, args):
        """Handle a client"""
        (client, address) = args
        self._connected_clients[client] = None
        try:
            message = pickle.loads(client.recv(2048))
            while message:
                if message._type == Message.MessageType.signup:
                    self.sign_up(message, client)
                if message._type == Message.MessageType.login:
                    self.login(message, client)
                if message._type == Message.MessageType.join_group:
                    self.join_group(message, client)
                    
                message = pickle.loads(client.recv(2048))
        except:
            print("{0}".format(traceback.format_exception(*sys.exc_info())))
            print("Client disconnected")
            
        print("Exitting worker")

    def join_group(self, message, client):
        """ handles a client attempting to join a group """
        if client in self._connected_clients:
            user = self._connected_clients[client]
            group = message._payload
            #got user name, now need to add him to existing chat group
            if group in self._chat_groups:
                self._chat_groups[group].add_client(user, socket=client)
            else:
                self._chat_groups[group] = ChatGroup(group)
                self._chat_groups[group].add_client(user, socket=client)

            self.ack_client(client, True)
        else:
            print("Client has not logged in yet")
            self.ack_client(client, False)
            
            
    def sign_up(self, message, client):
        """handle user sign up"""
        while message._payload != "cancel":
            nameAvailable = False if message._payload in self._users else True
            self.ack_client(client, nameAvailable)

            if nameAvailable:
                break
            
            message = pickle.loads(client.recv(2048))
            
        if message._payload != "cancel":
            name = message._payload
            message = pickle.loads(client.recv(2048))
            salt = self.gen_salt()
            self._users[name] = [salt, hashlib.sha512((salt + message._payload).encode('utf-8')).hexdigest()]

        self.ack_client(client, True)

        print(self._users)

    def login(self, message, client):
        success = False

        while message._target != "cancel":
            user = message._target
            psw = message._payload

            if user in self._users:
                uSalt = self._users[user][0]
                uHash = self._users[user][1]
                
                if uHash == hashlib.sha512((uSalt + psw).encode('utf-8')).hexdigest():
                    success = True
                    self._connected_clients[client] = user

                print("{0}: {1}".format(user, psw))
                self.ack_client(client, success)

                if not success:
                    message = pickle.loads(client.recv(2048))
                else:
                    break

    def gen_salt(self):
        alpha = "0123456790abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ~!@#$%^&*()-=_+`"
        return ''.join(random.choice(alpha) for i in range(16))
        
    def ack_client(self, client, ack):
        response = Message(mType=Message.MessageType.confirmation, mPayload=ack)
        client.send(pickle.dumps(response))            

    def __del__(self):
        """ destructor for chat server """        
        try:
            with open('u.txt', 'w') as out:
                json.dump(self._users, out)
            self._socket.close()
        except:
            print("Error closing socket. May not have been initialized")
        finally:
            print("Server exitting.")

                    
class Client:
    """Representation of a client"""
    def __init__(self, socket):
        self._user = ""
        self._groups = []
        """Client Constructor"""

class ChatGroup:
    """Representation of a chat group"""
    def __init__(self, name):
        """ constructor for ChatGroup """
        self._clients = {}
        self._name = name

    def send_all(self, message):
        """  """
        try:
            message = Message(mType=Message.MessageType.message, mPayload=message)
            for client, socket in self._clients.items():
                socket.send(pickle.dumps(message))
                                
        except:
            print("Error sending message to chat group {0}.".format(str(self._name)))

    def add_client(self, user_name, socket):
        self._clients[user_name] = socket

    def remove_client(self, user_name):
        if user_name in self._clients:
            self._clients[user_name] = None
