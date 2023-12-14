import requests
import os
import socket
from pathlib import Path
from decouple import config
import json
from file_send import file_send
from file_remove import remove
from file_read import read_file
from consensus_check import vote_from_terminal

    

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
            print("voted yes")
            vote_from_terminal(vote, "127.0.0.1", 8000, "127.0.0.1", 8000)
            exit()

        elif choice == "2":
            vote = False
            print("voted no")
            vote_from_terminal(vote, "127.0.0.1", 8000, "127.0.0.1", 8000)
            exit()

        else:
            print("Invalid argument provided. Please select one of the options that is offered.")
            print("")




#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
# MARK: Main
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()