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

        my_options=[('a', 'sign up'),
                 ('b', 'login'),
                 ('c', 'exit')]

        menu = Menu(title="chitter chat:",
                    options=my_options)
        
        choice = menu.get_option()
        while choice != 'c':
            if choice == 'a':
                self.sign_up()
            elif choice == 'b':
                self.login()
            elif choice == 'c':
                self.close()
            choice = menu.get_option()

        '''
        userIn = input(">>: ")
        while userIn != "/exit":
            message = Message(target="my group", mType=Message.MessageType.signup, mPayload=userIn)
            self._socket.send( pickle.dumps(message))
            userIn = input(">>: ")
        '''    
            
    def sign_up(self):
        user = input("Please enter a user name (\"cancel\" to cancel): ")
        response = self.request_user(user)

        print(user)
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
        print("login!")

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
                print("Invalid choice", end='')
                self.three_dots()

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
