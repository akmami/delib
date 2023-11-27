import os
import socket
from pathlib import Path
from decouple import config
import json
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--filepath", help="filepath that will be send from node to node")
parser.add_argument("--sender_ip", help="Sender node's IP address")
parser.add_argument("--sender_port", type=int, help="Sender node's port number")
parser.add_argument("--receiver_ip", help="Receiver node's IP address")
parser.add_argument("--receiver_port", type=int, help="Receiver node's port number")
args = parser.parse_args()


BUFFER_SIZE = config("BUFFER_SIZE", cast=int)


def send(filepath, sender_ip, sender_port, receiver_ip, receiver_port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((sender_ip, sender_port))
    
    filename = Path(filepath).name      # This is test file. Please either copy this to main directory ob delib project or change something else
    filesize = os.path.getsize(filepath)
    
    s.sendall( json.dumps({"func": "file_transfer", "filename": filename, "receiver_ip": receiver_ip, "receiver_port": receiver_port}).encode() )
    
    print("sending {}  bytes {} size of to {}:{}".format(filepath, filesize, receiver_ip, receiver_port) )    
    
    with open(filepath, "rb") as f:
        
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:          # if file transmitting is done
                s.send(b"DONE")         # default message to let receiver that file sharing is done
                break
            s.send(bytes_read)
        s.shutdown(1)                   # default signal to shutdown file send/receive
    s.close()


#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
# MARK: Main
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
if __name__ == "__main__":
    send(args.filepath, args.sender_ip, args.sender_port, args.receiver_ip, args.receiver_port)