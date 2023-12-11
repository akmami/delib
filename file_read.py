import os
import socket
from pathlib import Path
from decouple import config
import json
import argparse

BUFFER_SIZE = config("BUFFER_SIZE", cast=int)   # send 4096 bytes each time step
TRY_COUNT = config("TRY_COUNT", cast=int)       # try count to send request
TCP_PORT = config("TCP_PORT", cast=int)
UDP_PORT = config("UDP_PORT", cast=int)
LIBRARY_DIR = config("LIBRARY_DIR")
TEMP_DIR = config("TEMP")
NETWORK_IP = config("NETWORK_IP")


parser = argparse.ArgumentParser()
parser.add_argument("--filepath", help="filepath that will be send from node to node")
parser.add_argument("--sender_ip", help="Sender node's IP address")
parser.add_argument("--sender_port", type=int, help="Sender node's port number")
parser.add_argument("--receiver_ip", help="Receiver node's IP address")
parser.add_argument("--receiver_port", type=int, help="Receiver node's port number")
args = parser.parse_args()


BUFFER_SIZE = config("BUFFER_SIZE", cast=int)


def read_file(filepath, sender_ip, sender_port, receiver_ip, receiver_port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.connect((receiver_ip, sender_port))
    
    file_path = os.path.join(LIBRARY_DIR, filepath)
    print(file_path)

    data = {"func": "t_read_file", "filename": filepath, "receiver_ip": receiver_ip, "receiver_port": receiver_port}
    s.sendall( json.dumps(data).encode() )
    
    # Get the file
    with open(file_path, "r") as f:
        file_line = f.read()     # read 4096 bytes from the socket (receive)

    return file_line
    
    print("sending {} to {}:{}".format(filepath, receiver_ip, receiver_port) )    
    s.shutdown(1)                   # default signal to shutdown file send/receive
    s.close()


#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
# MARK: Main
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
if __name__ == "__main__":
    send(args.filepath, args.sender_ip, args.sender_port, args.receiver_ip, args.receiver_port)