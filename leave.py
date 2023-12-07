import os
import socket
from pathlib import Path
from decouple import config
import json


BUFFER_SIZE = config("BUFFER_SIZE", cast=int)
TCP_PORT = config("TCP_PORT", cast=int)

def send():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect( ("127.0.1.1", TCP_PORT) )
    s.sendall( json.dumps( {"func": "t_leave_request"} ).encode() )
    s.close()


#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
# MARK: Main
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
if __name__ == "__main__":
    send()