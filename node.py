import selectors
import socket
import time
import os
import shutil
import json
from decouple import config
import logging
import requests

# Use a web service to get the public IP address
response = requests.get('https://api64.ipify.org?format=json')
PUBLIC_IP = response.json()['ip']

logging.info( "The public IP address is {}".format(PUBLIC_IP) )


BUFFER_SIZE = config("BUFFER_SIZE", cast=int)   # send 4096 bytes each time step
TRY_COUNT = config("TRY_COUNT", cast=int)       # try count to send request
TCP_PORT = config("TCP_PORT", cast=int)
UDP_PORT = config("UDP_PORT", cast=int)
LIBRARY_DIR = config("LIBRARY_DIR")
TEMP_DIR = config("TEMP")
NETWORK_IP = config("NETWORK_IP")

logging.getLogger().setLevel(logging.INFO)      # INFO logs enabled

CWD = os.getcwd()                               # get current working directory
IP_ADDRESS = PUBLIC_IP                          # get IP address
LIBRARY_DIR = os.path.join(CWD, LIBRARY_DIR)    # get full directory for library folder
TEMP_DIR = os.path.join(CWD, TEMP_DIR)          # get full directory for temp folder.
                                                # this will be used to store temp files in case file transfer is needed


if not os.path.exists(LIBRARY_DIR):             # all items in node will be stored under library folder
    os.mkdir(LIBRARY_DIR)


if not os.path.exists(TEMP_DIR):                # all temp items in node will be stored under temp folder
    os.mkdir(TEMP_DIR)


class Node:
    def __init__(self, ip=None):
        self.ip = IP_ADDRESS
        self.ips = [IP_ADDRESS]
        self.library = []

        logging.info("New node created with IP: {} TCP port: {}, UDP port: {}".format(self.ip, TCP_PORT, UDP_PORT))

        if ip is not None:
            socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)     # if port was available, then it will reuse it
            
            logging.info( "Binding to IP: {}".format(ip) )

            socket_tcp.connect((ip, TCP_PORT))    

            socket_tcp.sendall( json.dumps({"func": "t_join_request", "ip": IP_ADDRESS}).encode("utf-8") )

            data = socket_tcp.recv(BUFFER_SIZE)
            self.ips = json.loads(data)

            logging.info("Successfully joined to the DS. IPs: {}".format(self.ips))

            socket_tcp.close()


    def run(self, t_sec=31536000):                                  # default end time is set to 1 year = 31536000

        selector = selectors.DefaultSelector()

        # Create TCP socket
        socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_tcp.settimeout(0.2)
        socket_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)     # if port was available, then it will reuse it
        socket_tcp.bind((NETWORK_IP, TCP_PORT))
        socket_tcp.listen(3)                                                 # max number of requests can wait in the queue

        # Create UDP socket
        socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        socket_udp.settimeout(0.2)
        socket_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)     # if port is not available, then it will reuse it
        socket_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)     # enable broadcasting
        socket_udp.bind((NETWORK_IP, UDP_PORT))

        # Register TCP and UDP sockets to the selector
        selector.register(socket_tcp, selectors.EVENT_READ)
        selector.register(socket_udp, selectors.EVENT_READ)

        t_end = time.time() + t_sec
        done = False

        try:
            while not done and time.time() < t_end:
                
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
                        if data["func"] == "t_print_message":
                            logging.info( "Message received from {}, message: {}".format(addr, data["text"]) )
                        
                        if data["func"] == "t_send_message":
                            receiver_ip = data["receiver_ip"]
                            message_socket = socket.socket()
                            message_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                            message_socket.connect((receiver_ip, TCP_PORT))
                            message_socket.sendall( json.dumps({"func": "t_print_message", "text": "Hi delib user. I wanted to greet you fucker!"}).encode() )
                            message_socket.close()
                        
                        if data["func"] == "t_save_ip":
                            new_ip = data["ip"]
                            self.ips.append(new_ip)
                            self.ips.sort()
                            logging.info( "New IP added to the list. Current IPs: {}".format(self.ips) )
                            
                        if data["func"] == "t_join_request":
                            new_ip = data["ip"]
                            
                            for ip in self.ips:
                                if not ip == IP_ADDRESS:
                                    message_socket = socket.socket()
                                    message_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                                    message_socket.connect((ip, TCP_PORT))
                                    message_socket.sendall( json.dumps({"func": "t_save_ip", "ip": new_ip}).encode("utf-8") )
                                    message_socket.close()

                            self.ips.append(new_ip)
                            self.ips.sort()
                            conn.sendall( json.dumps(self.ips).encode("utf-8") )
                            logging.info( "New IP added to the list. Current IPs: {}".format(self.ips) )
                        
                        elif data["func"] == "t_remove_ip":
                            ip = data["ip"]
                            self.ips.remove(ip)
                            self.ips.sort()
                            logging.info( "IP removed from the list. Current IPs: {}".format(self.ips) )

                        elif data["func"] == "t_leave_request":

                            for ip in self.ips:
                                if not ip == IP_ADDRESS:
                                    leave_socket = socket.socket()
                                    leave_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                                    leave_socket.connect( (ip, TCP_PORT) )
                                    leave_socket.sendall( json.dumps({"func": "t_remove_ip", "ip": IP_ADDRESS}).encode("utf-8") )
                                    leave_socket.close()

                            logging.info( "You have been removed from DS successfully." )
                            
                            if os.path.isdir(LIBRARY_DIR):
                                shutil.rmtree(LIBRARY_DIR)
                            if os.path.isdir(TEMP_DIR):
                                shutil.rmtree(TEMP_DIR)
                            
                            done = True
                            
                            logging.info( "Local files deleted successfuly. See you." )

                            break
                        
                        elif data["func"] == "t_store_file":
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
                        
                        elif data["func"] == "t_remove_file":
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

                        if data["func"] == "b_add_ip":
                            new_ip = data["ip"]
                            self.ips.append(new_ip)
                            logging.info( "New IP added to the list. Current IPs: {}".format(self.ips) )
                        
                        elif data["func"] == "b_remove_ip":
                            ip = data["ip"]
                            self.ips.remove(ip)
                            self.ips.sort()
                            logging.info( "IP removed from the list. Current IPs: {}".format(self.ips) )
                        
                        # close connection
                        conn.close()

        except KeyboardInterrupt:
            logging.info("Server terminated from keyboard.")

        # Close remaining sockets and unregister them
        selector.unregister(socket_tcp)
        socket_tcp.close()
        selector.unregister(socket_udp)
        socket_udp.close()

        selector.close()               
        
        logging.info( "Thread execution ended for node. Waiting for the last 5 seconds" )
        
        time.sleep(5)