import selectors
import socket
import time
import os
import shutil
import json
from decouple import config
import logging


BUFFER_SIZE = config("BUFFER_SIZE", cast=int)   # send 4096 bytes each time step
TRY_COUNT = config("TRY_COUNT", cast=int)       # try count to send request
TCP_PORT = config("TCP_PORT", cast=int)
UDP_PORT = config("UDP_PORT", cast=int)
LIBRARY_DIR = config("LIBRARY_DIR")
TEMP_DIR = config("TEMP")

logging.getLogger().setLevel(logging.INFO)      # INFO logs enabled

CWD = os.getcwd()                               # get current working directory
HOSTNAME = socket.gethostname()                 # get hostname 
IP_ADDRESS = socket.gethostbyname(HOSTNAME)     # get IP address
LIBRARY_DIR = os.path.join(CWD, LIBRARY_DIR)    # get full directory for library folder
TEMP_DIR = os.path.join(CWD, TEMP_DIR)          # get full directory for temp folder.
                                                # this will be used to store temp files in case file transfer is needed


if not os.path.exists(LIBRARY_DIR):             # all items in node will be stored under library folder
    os.mkdir(LIBRARY_DIR)


if not os.path.exists(TEMP_DIR):                # all temp items in node will be stored under temp folder
    os.mkdir(TEMP_DIR)


class Node:
    def __init__(self):
        self.ip = IP_ADDRESS
        self.ips = []
        self.library = []

        logging.info("New node created with IP: {} TCP port: {}, UDP port: {}".format(self.ip, TCP_PORT, UDP_PORT))


    def run(self, t_sec=31536000):                                  # default end time is set to 1 year = 31536000

        selector = selectors.DefaultSelector()

        # Create TCP socket
        socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_tcp.settimeout(0.2)                                           # set timeout to 0.2 seconds
        socket_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)     # if port was available, then it will reuse it
        socket_tcp.bind((self.ip, TCP_PORT))
        socket_tcp.listen(3)                                                 # max number of requests can wait in the queue

        # Create UDP socket
        socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        socket_udp.settimeout(0.2)
        socket_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)     # if port is not available, then it will reuse it
        socket_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)     # enable broadcasting
        socket_udp.bind((self.ip, UDP_PORT))

        # Register TCP and UDP sockets to the selector
        selector.register(socket_tcp, selectors.EVENT_READ)
        selector.register(socket_udp, selectors.EVENT_READ)

        t_end = time.time() + t_sec

        try:
            while time.time() < t_end:
                events = selector.select()

                for key, _ in events:
                    
                    if key.fileobj == socket_tcp:           # messages received by TCP protocol

                        (conn, addr) = key.fileobj.accept()
                        data = conn.recv(BUFFER_SIZE)       # receive data from client
                        data = json.loads(data)

                        if "func" not in data:
                            logging.warning("Request received which does not contain 'func' tag.")
                            continue

                        logging.info( "Request with func: '{}' received from socket channel.".format( data["func"] ) )


                        # --------------------------------------------------------------------------------------------
                        # --------------------------------------------------------------------------------------------
                        # execute requested func
                        # --------------------------------------------------------------------------------------------
                        # --------------------------------------------------------------------------------------------
                        if data["func"] == "print_message":
                            logging.info( "Message received from {}, message: {}".format(addr, data["text"]) )

                        elif data["func"] == "leave":
                            for ip in self.ips:
                                socket_udp.sendto( {"func": "remove_ip", "ip": self.ip}.encode("utf-8"), (ip, UDP_PORT) )
                            logging.info( "You have been removed from DS successfully." )

                            if os.path.isdir(LIBRARY_DIR):
                                shutil.rmtree(LIBRARY_DIR)
                            if os.path.isdir(TEMP_DIR):
                                shutil.rmtree(TEMP_DIR)
                            
                            logging.info( "Local files deleted successfuly. See you." )
                        
                        elif data["func"] == "store_file":
                            filename = data["filename"]
                            filepath = os.path.join(LIBRARY_DIR, filename)
                            
                            # Get the file
                            with open(filepath, "wb") as f:
                                while True:
                                    bytes_read = conn.recv(BUFFER_SIZE)     # read 4096 bytes from the socket (receive)
                                    if bytes_read == b"DONE":               # if sender sends DONE signal then it is done.
                                        self.library.append(filename)       # add to list
                                        logging.info( "File with filename {} received and stored successfully.".format(filename) )
                                        break
                                    
                                    f.write(bytes_read)                     # write to the file the bytes we just received
                                conn.shutdown(1)
                        
                        elif data["func"] == "remove_file":
                            filename = data["filename"]
                            filepath = os.path.join(LIBRARY_DIR, filename)

                            self.library.remove(filename)                   # remove from list
                            os.remove(filepath)                             # remove file
                            logging.info( "File with filename {} removed successfully.".format(filename) )
                        
                        # close connection
                        conn.close()

                    elif key.fileobj == socket_udp:
                        (conn, addr) = key.fileobj.accept()
                        data = conn.recv(BUFFER_SIZE)
                        data = json.loads(data)

                        if data["func"] == "add_ip":
                            new_ip = data["ip"]
                            self.ips.append(new_ip)
                            logging.info( "New IP added to the list. Current IPs: {}".format(self.ips) )
                        
                        elif data["func"] == "remove_ip":
                            ip = data["ip"]
                            self.ips.remove(ip)
                            logging.info( "IP removed from the list. Current IPs: {}".format(self.ips) )
                        
                        # close connection
                        conn.close()


        except KeyboardInterrupt:
            logging.info("Server terminated from keyboard.")

        finally:
            # Close remaining sockets and unregister them
            selector.unregister(socket_tcp)
            socket_tcp.close()

            selector.unregister(socket_udp)
            socket_udp.close()

            selector.close()               
        
        logging.info( "Thread execution ended for node. Waiting for the last 5 seconds" )
        
        time.sleep(5)