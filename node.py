import socket


hostname = socket.gethostname()
ipaddress = socket.gethostbyname(hostname)


class Node:
    def __init__(self, ip=ipaddress, port=8001, ips=[ipaddress], library=[]):
        self.ip = ip
        self.port = port
        self.ips = ips
        self.library = library
