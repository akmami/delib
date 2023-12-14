import requests
import os
import socket
from pathlib import Path
from decouple import config
import json
from file_send import file_send
from file_remove import remove
from file_read import read_file

    

#Adding code here
response = requests.get('https://httpbin.org/ip')
ip_data = response.json()
public_ip = ip_data['origin']

BUFFER_SIZE = config("BUFFER_SIZE", cast=int)
TCP_PORT = config("TCP_PORT", cast=int)

vote = False

def main():
    print("Welcome to Online Library Catalog Stored in Decentralised Network (delib)")
    print("")

    while True:
        print("Please vote for candidate node:")
        print("\t1. Yes")
        print("\t2. No")
        print("")
        choice = input("> ").strip()

        if choice == "1":
            vote = True
            vote_from_terminal(vote, public_ip, 8000, public_ip, 8000)
            exit()

        elif choice == "2":
            vote = False
            vote_from_terminal(vote, public_ip, 8000, public_ip, 8000)
            exit()

        else:
            print("Invalid argument provided. Please select one of the options that is offered.")
            print("")

def vote_from_terminal(vote, sender_ip, sender_port, receiver_ip, receiver_port):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.connect((receiver_ip, sender_port))

    data = {"func": "t_vote_from_terminal", "vote": vote}
    s.sendall( json.dumps(data).encode() )
    
    print("Vote sent.")    
    s.shutdown(1)                   # default signal to shutdown file send/receive
    s.close()



#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
# MARK: Main
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()