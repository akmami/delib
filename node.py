import socket
import time

hostname = socket.gethostname()
ipaddress = socket.gethostbyname(hostname)


ENTRY_PORT = 8001 # logically setting this node as entry point as it will send data for the rest of the nodes.

class Node:
    def __init__(self, ip=ipaddress, port=8001, ips=[ipaddress], library=[]):
        self.ip = ip
        self.port = port
        self.ips = ips
        self.library = library

    def run(self, forever=False, t_sec=10):
            
        t_end = time.time() + t_sec

        if self.port == ENTRY_PORT:

            while forever or time.time() < t_end:
                for port in self.ips:
                    if self.port == port: # do not send to itself
                        continue
                    while True:
                        try: 
                            s = socket.socket()
                            s.connect((self.ip, port))
                            s.sendall("Hello there".encode())
                            s.close()
                            break
                        except:
                            if forever or time.time() < t_end: 
                                break
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("binding to {}".format(self.port))
            s.settimeout(0.2) # set timeout to 0.2 seconds
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.ip, self.port))
            s.listen(3) # max number of requests can wait in the queue

            while forever or time.time() < t_end:    
                try:            
                    (conn, addr) = s.accept()
                    data = conn.recv(1024) # receive data from client
                    print( data.decode() + ' server-port=' + str(self.port) )
                    # you can return data as a reply
                    # conn.send("Thank you".encode())
                    conn.close()
                except socket.timeout:
                    pass
            
            s.close()
        
        print("Thread execution ended for node with port {}. Waiting for the last 5 seconds".format(self.port))
        
        time.sleep(5)