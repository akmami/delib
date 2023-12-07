import os
import socket
from pathlib import Path
from decouple import config
import json
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--receiver_ip", help="Receiver node's IP address")
args = parser.parse_args()


BUFFER_SIZE = config("BUFFER_SIZE", cast=int)
TCP_PORT = config("TCP_PORT", cast=int)

def send(receiver_ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect( ("127.0.1.1", TCP_PORT) )
    s.sendall( json.dumps( {"func": "t_send_message", "receiver_ip": receiver_ip}).encode() )
    s.close()


#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
# MARK: Main
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
if __name__ == "__main__":
    send(args.receiver_ip)