import sys
import numbers
from chat_server import ChatServer

def main(args=None):
    """Entry point for chat_server"""
    
    if len(sys.argv) != 2:
        print("Invalid usage. Usage:")
        print("{0} [port_number]".format(sys.argv[0]))
    else:
        try:
            port = int(sys.argv[1]);
            
            if port > 1024 and port <= 65535:
                server = ChatServer(port)
                server.start_server()
            else:
                print("Please specify a port between 1025 and 65535")
                print("Ports 1-1024 are used by common applications...")
                
        except ValueError:
            print("%s is not a valid port number." % sys.argv[1])
        finally:
            print("Exitting...")
            
if __name__ == "__main__":
    main()
