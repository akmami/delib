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

def ask_vote_for_cand_node(cand_node_ip, sender_ip, sender_port, receiver_ip, receiver_port):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.connect((receiver_ip, sender_port))

    data = {"func": "t_ask_vote_cand_node", "cand_node_ip": cand_node_ip, "receiver_ip": receiver_ip, "receiver_port": receiver_port}
    s.sendall( json.dumps(data).encode() )
    
    print("asking vote for candidate node {} - from {}:{}".format(cand_node_ip, receiver_ip, receiver_port) )    
    s.shutdown(1)                   # default signal to shutdown file send/receive
    s.close()

def send_vote(vote, cand_node_ip, sender_ip, sender_port, receiver_ip, receiver_port):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.connect((receiver_ip, sender_port))

    data = {"func": "t_send_vote", "vote": vote, "cand_node_ip": cand_node_ip, "sender_ip": sender_ip, "sender_port": sender_port, "receiver_ip": receiver_ip, "receiver_port": receiver_port}
    s.sendall( json.dumps(data).encode() )
    
    print("sending vote for candidate node {} - to {}:{}".format(cand_node_ip, receiver_ip, receiver_port) )    
    s.shutdown(1)                   # default signal to shutdown file send/receive
    s.close()

#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
# MARK: Main
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
if __name__ == "__main__":
    send(args.filepath, args.sender_ip, args.sender_port, args.receiver_ip, args.receiver_port)