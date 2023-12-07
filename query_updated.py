#set PYTHONHASHSEED=0
from typing import Final
import os 


MAX_NODE: Final = 50 


def query(file_name,port, nodes):
    def_file_path = "C:\\Users\\Lenovo\\Desktop\\parallel\\files"

    #Getting hash value from file name
    q_value = hash(file_name)%MAX_NODE
    print(q_value)

    #Sort nodes list
    nodes.sort()

    #Check where file is supposed to be
    for i in nodes:
        if(q_value < nodes[len(nodes)-1]) and q_value > nodes[0]:
            if(q_value <= i):
                split_index = i
                query_nodes = nodes[nodes.index(i): len(nodes)] + nodes[0:len(nodes)-nodes.index(i)]
                print(query_nodes)
                break
        else:
            query_nodes = nodes
            print(query_nodes)
            break
        

        #Parameter to check if file exists or not
    control = 0

    #Check where file is supposed to be
    for i in query_nodes:
        query_node = i
        check_path = (def_file_path + "\\" + str(query_node) + "\\" +file_name)
        control=1
        #Here we are supposed to send the file name to the ip/port that has the id of query_node and get an answer. If answer id 1 then make control 1 and stop searching
        break
    if(control==1):
        print(file_name, " READ SUCCESFULLY")
    else:
        print(file_name, " DOES NOT EXIST IN THIS SYSTEM")


    



node_list = [40,10,13,37] 
request_node = 8000         #This should be IP later on and it should connect us to the node list of the system
query("a.txt", request_node, node_list)
#query("b.txt", request_node, node_list)
#query("c.txt", request_node, node_list)
#query("d.txt", request_node, node_list)
#query("f.txt", request_node, node_list)
#query("f43.txt", request_node, node_list)
#query("6000.txt", request_node, node_list)