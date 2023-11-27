import socket
import time
import os 
import json


HOSTNAME = socket.gethostname()
IP_ADDRESS = socket.gethostbyname(HOSTNAME)
PORT = 8001

DATA_DIR = os.path.join("data")
if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)
# FILES_PATH = os.path.join("data", "delib") # TODO: uncomment this on prod

BUFFER_SIZE = 4096 # send 4096 bytes each time step

class Node:
    def __init__(self, ip=IP_ADDRESS, port=PORT, ips=[IP_ADDRESS]):
        self.ip = ip
        self.port = port
        self.ips = ips
        self.library = []

        DELIB_PATH = os.path.join("data", "delib-{}-{}".format(ip, port)) # TODO: delete this on prod

        if not os.path.exists(DELIB_PATH):
            os.mkdir(DELIB_PATH)


    def run(self, t_sec=10): # TODO: default end time is set to 1 year = 31536000
            
        t_end = time.time() + t_sec

        done = False

        while not done and time.time() < t_end:  
            if self.port == PORT:
                
                count = 0

                for port in self.ips:
                    
                    if self.port == port: # do not send to itself
                        continue
             
                    try: 
                        s = socket.socket()
                        s.connect((self.ip, port))
                        # s.sendall( json.dumps({"func": "print", "text": "Hello there"}).encode() )
                        filename = "Slides-06-Communication.pdf"
                        filesize = os.path.getsize(os.path.join(os.getcwd(), filename))
                        s.sendall( json.dumps({"func": "file_transfer", "filename": filename, "filesize": filesize}).encode() )
                        print("sending " + os.path.join(os.getcwd(), filename) + " size of " + str(filesize))
                        
                        with open(os.path.join(os.getcwd(), filename), "rb") as f:
                            
                            bytes_read = f.read(BUFFER_SIZE)
                            if not bytes_read:          # file transmitting is done
                                break
                            s.send(bytes_read)
                        s.send(b"DONE")
                        s.shutdown(1)
                        s.close()
                        count += 1
                        if count == len(self.ips) - 1:
                            done = True
                    except Exception as e: 
                        print(e)
            else:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print("binding to {}".format(self.port))
                s.settimeout(2) # set timeout to 0.2 seconds
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((self.ip, self.port))
                s.listen(3) # max number of requests can wait in the queue

                while time.time() < t_end:    
                    try:            
                        (conn, addr) = s.accept()
                        data = conn.recv(BUFFER_SIZE).decode('utf-8') # receive data from client
                        data = json.loads(data)

                        if data["func"] == "print":
                            print( data["text"] + ' server-port=' + str(self.port) )
                            conn.close()
                        elif data["func"] == "file_transfer":
                            filename = data["filename"]
                            filesize = data["filesize"]
                            delib_path = os.path.join(os.getcwd(), "data", "delib-{}-{}".format(self.ip, self.port), filename)
                            print("{} {} {}".format(filename, filesize, delib_path))
                            filename = os.path.join(os.getcwd(), "data", "delib-{}-{}".format(self.ip, self.port), filename)
                            with open(filename, "wb") as f:
                                while True:
                                    # read 1024 bytes from the socket (receive)
                                    bytes_read = conn.recv(BUFFER_SIZE)
                                    if bytes_read == b"DONE":
                                        print("Done Receiving.")
                                        break
                                    # write to the file the bytes we just received
                                    f.write(bytes_read)
                            
                                conn.shutdown(1)
                                # you can return data as a reply
                                # conn.send("Thank you".encode())
                                conn.close()
                        break
                    except socket.timeout:
                        pass
                
                s.close()
        
        print("Thread execution ended for node with port {}. Waiting for the last 5 seconds".format(self.port))
        
        time.sleep(5)