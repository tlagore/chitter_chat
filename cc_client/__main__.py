import sys
import re
from chat_client import ChatClient, IPFormat


def main(args=None):
    """Entry point for chat_client"""
    ipFormat = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
    # request this from user at a later point
    if len(sys.argv) != 3:
        print("Invalid usage. Usage:")
        print("{0} [server_address] [port]".format(sys.argv[0]))
    else:
        try:
            host = str(sys.argv[1])
            if not re.match(ipFormat, host):
                raise IPFormat("Invalid IP format")
            
            port = int(sys.argv[2])
            client = ChatClient(host, port)
        except ValueError:
            print("{0} is not a valid port number.".format(sys.argv[2]))
        except IPFormat:
            print("{0} is not a valid ip number.".format(sys.argv[1]))
        finally:
            print("Exitting...")


if __name__ == "__main__":
    main()
