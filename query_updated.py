#set PYTHONHASHSEED=0
from typing import Final
import os 
import hashlib
import ipaddress

def hash_file_name(file_name):
    # Create a SHA-256 hash object
    hash_object = hashlib.sha256()

    # Update the hash object with the bytes of the file name
    hash_object.update(file_name.encode())

    # Get the integer representation of the hash
    hashed_file_name_int = int(hash_object.hexdigest(), 16)

    return hashed_file_name_int


MAX_NODE: Final = 100 

"""""

def query(file_name,port, nodes_unsorted):
    def_file_path = "C:\\Users\\Lenovo\\Desktop\\parallel\\files"

    q_value = hash_file_name(file_name)%MAX_NODE
    print(q_value)


    #Sort nodes list
    # Convert IP addresses to integers
    ip_integers = [int(ipaddress.IPv4Address(ip))%MAX_NODE for ip in nodes_unsorted]

    # Sort the list of IP addresses based on their integer values
    nodes = [ip for _, ip in sorted(zip(ip_integers, nodes_unsorted))]

    for i in nodes:
        print(i, " - ", int(ipaddress.IPv4Address(i))%MAX_NODE)
    #Check where file is supposed to be
    for i in nodes:
        if(q_value <= int(ipaddress.IPv4Address(nodes[len(nodes)-1]))%MAX_NODE) and (q_value > int(ipaddress.IPv4Address(nodes[0]))%MAX_NODE):
            if(q_value <= int(ipaddress.IPv4Address(i))%MAX_NODE):
                split_index = i
                print(nodes.index(i))
                query_nodes = nodes[nodes.index(i): len(nodes)] + nodes[0:len(nodes)-nodes.index(i)]
                print(query_nodes)
                break
        else:
            print("HI")
            query_nodes = nodes
            print(query_nodes)
            break
        


    
"""


#node_list = ["139.179.103.153","139.179.103.26", "139.179.103.5","139.179.103.2","139.179.103.10"] 
#node_list = ["139.179.103.153","139.179.103.10"] 
#request_node = 8000         #This should be IP later on and it should connect us to the node list of the system
#query("f.txt", request_node, node_list)
#query("b.txt", request_node, node_list)
#query("c.txt", request_node, node_list)
#query("d.txt", request_node, node_list)
#query("f.txt", request_node, node_list)
#query("f43.txt", request_node, node_list)
#query("6000.txt", request_node, node_list)