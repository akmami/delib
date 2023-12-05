#set PYTHONHASHSEED=0
from typing import Final
import os 


MAX_NODE: Final = 50 


def query(file_name,port, nodes):
    def_file_path = "C:\\Users\\Lenovo\\Desktop\\parallel\\files"

    #Getting hash value from file name
    q_value = hash(file_name)%MAX_NODE

    #Sort nodes list
    nodes.sort()

    #Parameter to check if file exists or not
    control = 0

    #Check where file is supposed to be
    for i in nodes:
        if(q_value<=i):
            query_node = i
            check_path = (def_file_path + "\\" + str(query_node) + "\\" +file_name)
            if(os.path.exists(check_path)):
                file = open(check_path, "r")
                print(file.read())
                control = 1
                break
    if(control==1):
        print(file_name, " READ SUCCESFULLY")
    else:
        print(file_name, " DOES NOT EXIST IN THIS SYSTEM")
    
    
    #print("File is at node: ", query_node)
    #print(def_file_path + "\\" + str(query_node) + "\\" +file_name)



    



node_list = [40,10,13,37] 
request_node = 8000         #This should be IP later on and it should connect us to the node list of the system
query("a.txt", request_node, node_list)
query("b.txt", request_node, node_list)
query("c.txt", request_node, node_list)
query("d.txt", request_node, node_list)
query("f.txt", request_node, node_list)
query("f43.txt", request_node, node_list)
query("6000.txt", request_node, node_list)