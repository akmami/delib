import socket
import time
import os 
import json
from decouple import config


BUFFER_SIZE = config("BUFFER_SIZE", cast=int)   # send 4096 bytes each time step
TRY_COUNT = config("TRY_COUNT", cast=int)       # try count to send request
PORT = config("PORT", cast=int)
DATA_PATH = config("DATA_PATH")

CWD = os.getcwd()
HOSTNAME = socket.gethostname()
IP_ADDRESS = socket.gethostbyname(HOSTNAME)
DATA_DIR = os.path.join(DATA_PATH)

if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)

# FILES_PATH = os.path.join("data", "delib")    # TODO: uncomment this on prod


class Node:
    def __init__(self, ip=IP_ADDRESS, port=PORT, ips=[IP_ADDRESS]):
        self.ip = ip
        self.port = port
        self.ips = ips
        self.library = []

        DELIB_PATH = os.path.join(CWD, "data", "delib-{}-{}".format(ip, port)) # TODO: delete this on prod

        if not os.path.exists(DELIB_PATH):
            os.mkdir(DELIB_PATH)

        print("IP {} port {}".format(ip, port))


    def run(self, t_sec=31536000): # TODO: default end time is set to 1 year = 31536000

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.2)                                           # set timeout to 0.2 seconds
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)     # if port is not available, then it will reuse it
        s.bind((self.ip, self.port))
        s.listen(3)                                                 # max number of requests can wait in the queue

        t_end = time.time() + t_sec

        while time.time() < t_end:    
            try:            
                (conn, addr) = s.accept()
                data = conn.recv(BUFFER_SIZE).decode('utf-8')       # receive data from client
                data = json.loads(data)

                if data["func"] == "print":
                    print( "Message received from {}, message: {}".format(addr, data["text"]) )
                    conn.close()
                
                elif data["func"] == "file_receive":
                    filename = data["filename"]
                    filepath = os.path.join(CWD, "data", "delib-{}-{}".format(self.ip, self.port), filename)
                    
                    # Get the file
                    with open(filepath, "wb") as f:
                        while True:
                            bytes_read = conn.recv(BUFFER_SIZE)     # read 4096 bytes from the socket (receive)
                            if bytes_read == b"DONE":               # if sender sends DONE signal then it is done.
                                break
                            
                            f.write(bytes_read)                     # write to the file the bytes we just received
                    
                        conn.shutdown(1)
                    conn.close()
                
                elif data["func"] == "file_transfer":
                    filename = data["filename"]
                    receiver_ip = data["receiver_ip"]
                    receiver_port = data ["receiver_port"]
                    filepath = os.path.join(CWD, "data", "delib-{}-{}".format(self.ip, self.port), filename)
                    
                    # Get the file
                    with open(filepath, "wb") as f:
                        while True:
                            bytes_read = conn.recv(BUFFER_SIZE)     # read 4096 bytes from the socket (receive)
                            if bytes_read == b"DONE":               # if sender sends DONE signal then it is done.
                                break
                            
                            f.write(bytes_read)                     # write to the file the bytes we just received
                    
                        conn.shutdown(1)
                    conn.close()

                    # Send to the receiver
                    sender_socket = socket.socket()
                    sender_socket.connect((receiver_ip, receiver_port))
                                        
                    sender_socket.sendall( json.dumps({"func": "file_receive", "filename": filename}).encode() )

                    filesize = os.path.getsize(filepath)
                    
                    print("sending {}  bytes {} size of to {}:{}".format(filepath, filesize, receiver_ip, receiver_port) )  
                    
                    with open(filepath, "rb") as f:
                        
                        while True:
                            bytes_read = f.read(BUFFER_SIZE)
                            if not bytes_read:                      # if file transmitting is done
                                s.send(b"DONE")                     # default message to let receiver that file sharing is done
                                break
                            sender_socket.send(bytes_read)
                        sender_socket.shutdown(1)                   # default signal to shutdown file send/receive
                    sender_socket.close()
                    
                    # delete local file
                    os.remove(filepath)
                break
            except socket.timeout:                                  # 0.2 seconds
                pass
        
        s.close()
        
        print("Thread execution ended for node with port {}. Waiting for the last 5 seconds".format(self.port))
        
        time.sleep(5)