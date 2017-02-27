from getpass import getpass
import os
import pickle
import platform
import socket
import sys
import threading
import time

from message import Message

class ChatClient:
    """Chat server class to handle chat server interactions"""

    def __init__(self, host, port):
        """constructor for chat client"""
        print("{0} {1}".format(host, port))

        self._user = None
        self._group = None

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((host, port))

        self._listenServer = threading.Thread(target=self.listen_server)
        self._listenClient = threading.Thread(target=self.listen_client)
        
        self._listenServer.start()
        self._listenClient.start()

        self._listenServer.join()
        self._listenClient.join()

    def listen_server(self):
        """listens for interaction from the server"""
        #message = self._socket.recv(2048)
        #while message:
            #print(message)
            #message = self._socket.recv(2048)
                    
    def listen_client(self):
        """listen for client input to pass to the server"""
        my_options=[('s', 'sign up'),
                 ('l', 'login'),
                 ('q', 'quit')]

        menu = Menu(title="chitter chat:",
                    options=my_options)
        
        choice = menu.get_option()
        while choice != 'q':
            if choice == 's':
                self.sign_up()
            elif choice == 'l':
                self.login()
            elif choice == 'q':
                self.close()
            choice = menu.get_option()        

            
    def user_loop(self):
        """ menu loop for when user is logged in """
        if self._user is None:
            print("User must be logged in to use this feature.")
        else:
            my_options = [('j', 'join channel'),
                          ('l', 'logout'),
                          ('q', 'quit')]

            menu = Menu(title="{0}'s chitter chat".format(self._user),
                        options = my_options)

            choice = menu.get_option()
            while choice != 'q':
                  if choice == 'j':
                      self.join_group()
                  elif choice == 'l':
                      break
                  elif choice == 'q':
                      Menu.three_dots("Join channel!")
                  choice = menu.get_option()        

    def join_group(self):
        """ 
        handles client attempting to join a group
        """
        group = input("Please enter a group to join (\"cancel\" to cancel): ")
        message = Message(mType=Message.MessageType.join_group, mPayload=group)
        self._socket.send(pickle.dumps(message))
        response = pickle.loads(self._socket.recv(2048))
        while response._payload != True and message._payload != "cancel":
            print("Error joining channel.")
            group = input("Please enter a group to join (\"cancel\" to cancel): ")
            message = Message(mType=Message.MessageType.join_group, mPayload=group)
            self._socket.send(pickle.dumps(message))
            response = pickle.loads(self._socket.recv(2048))

            ##YOU WERE EDITING THIS FUNCTION

        if response._payload == True:
            self._group = group
            self.chat_loop()

    def chat_loop(self):
        if self._group is None:
            print("Group is not set...")
        else:
            print("chat loop! {0}".format(self._group))
            time.sleep(2)
        
    def serialize_message(m_type=None, m_payload=None, m_target=None):
        """ Haven't used yet, but might be useful to create a message
        and serialize in the same call """
        message = Message(mType=m_type, mPayload=m_payload, target=m_target)
        return pickle.dumps(message)
        
            
    def sign_up(self):
        """ 
        handles client side interaction of signing in to server
        
        checks with the server to ensure name is available
        """
        user = input("Please enter a user name (\"cancel\" to cancel): ")
        response = self.request_user(user)

        while response._payload != True and user != "cancel":
            print("User name is taken.")
            user = input("Please enter a user name (\"cancel\" to cancel): ")
            response = self.request_user(user)
        
        if user != "cancel":
            psw = getpass()
            psw2 = getpass(prompt="Repeat password: ")
            while psw != psw2:
                print("Passwords do not match")
                psw = getpass()
                psw2 = getpass(prompt="Repeat password: ")
                
            message = Message(mType=Message.MessageType.signup, mPayload=psw)
            self._socket.send(pickle.dumps(message))
            response = pickle.loads(self._socket.recv(2048))
        
            if response._payload:
                Menu.three_dots("Successfully signed up")
        else:
            Menu.three_dots("Cancelled signup process")
            
            
    def request_user(self, user):
        message = Message(mType=Message.MessageType.signup, mPayload=user)
        self._socket.send(pickle.dumps(message))
        response = pickle.loads(self._socket.recv(2048))
        return response
        
    def login(self):
        message = self.get_creds()
        self._socket.send(pickle.dumps(message))
        response = pickle.loads(self._socket.recv(2048))
        
        while response._payload != True:
            print("Invalid user or password.")
            message = self.get_creds()

            self._socket.send(pickle.dumps(message))
            response = pickle.loads(self._socket.recv(2048))
            
            if message._target == "cancel":
                break

        if message._target != "cancel":
            Menu.three_dots("Login successful")
            self._user = message._target
            self.user_loop()
            
        else:
            Menu.three_dots("Login cancelled")

    def get_creds(self):
        user = input("User name (\"cancel\" to abort): ")
        psw = getpass()
        message = Message(mType=Message.MessageType.login, target=user, mPayload=psw)
        return message
        
    def close(self):
        print("exit!")
    
    def __del__(self):
        """destructor for chat client"""

class IPFormat(Exception):
    """custom exception to indicate an IP format error"""
    
    def __init__(self, value):
        self._message = value

    def __str__(self):
        return repr(self._message)


class Menu:
    """ Handles a simple console based menu """
    def __init__(self, title="MainMenu", prompt="Please enter your choice: ", options=[]):
        """ 
        menu contructor
        if title and prompt are not specified, defaults are used

        options is a list of tuples instead of a dict in order to maintain 
        option order        
        """
        self._title = str(title)
        self._prompt = str(prompt)
        self._options = options

    def display_menu(self):
        """ displays the menu title and options """
        op_sys = platform.system()

        self.clear_screen()
        print(self._title)
        
        if self._options:
            for (key, value) in self._options:
                print("{0}: {1}".format(str(key), str(value)))
        else:
          print("No options in menu.")

    def get_option(self):
        """ 
        get_option displays the menu then gets an option from the user

        if the options are empty, then a message is displayed and get_option exits
        otherwise, the user is prompted for a choice until they choose a choice
        that exists in the menu
        """
        if self._options:
            self.display_menu()
            choice = input(self._prompt)
            choices = [ch for ch in self._options if ch[0] == choice]
            while not choices:
                self.three_dots(message="Invalid choice")

                self.display_menu()
                choice = input(self._prompt)
                choices = [ch for ch in self._options if ch[0] == choice]
                
            return choices[0][0]
        else:
            print("No options in menu.")

    @staticmethod
    def three_dots(message):
        """ prints 3 dots with a .5 second delay between each dot """
        print(message, end='')
        sys.stdout.flush()
        
        for i in range(0,3):
            print('.', end='')
            sys.stdout.flush()
            time.sleep(0.5)

        print()


    def clear_screen(self):
        """ clears the console based on the operating system """
        os_sys = platform.system()

        print("clear screen")
        if os_sys == "Linux":
            os.system('clear')
        else:
            os.system('cls')
