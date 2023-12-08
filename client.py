import requests
import os
import socket
from pathlib import Path
from decouple import config
import json

    

#Adding code here
response = requests.get('https://httpbin.org/ip')
ip_data = response.json()
public_ip = ip_data['origin']

BUFFER_SIZE = config("BUFFER_SIZE", cast=int)
TCP_PORT = config("TCP_PORT", cast=int)

def main():
    print("Welcome to Online Library Catalog Stored in Decentralised Network (delib)")
    print("")

    while True:
        print("Please select one of the optinons:")
        print("\t1. Add Document")
        print("\t2. Delete Document")
        print("\t3. Query")
        print("\t4. Exit")
        print("")
        choice = input("> ").strip()

        if choice == "1":
            #Adding code here
            print("Give file path:")
            read_file = input()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect( ("127.0.1.1", TCP_PORT) )
            s.sendall( json.dumps( {"func": "t_store_file", "filename": read_file} ).encode() )
            s.close()
        elif choice == "2":
            pass
        elif choice == "3":
            pass
        elif choice == "4":
            pass
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