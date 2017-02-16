import sys
from chat_client import ChatClient

def main(args=None):
    """Entry point for chat_client"""
    # request this from user at a later point
    host = '127.0.0.1'

    #request this from user at a later point
    port = 2727

    client = ChatClient(host, port)
    # entry code here


if __name__ == "__main__":
    main()
