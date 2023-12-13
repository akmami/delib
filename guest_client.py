import requests
import os
import socket
from pathlib import Path
from decouple import config
import json
from file_send import file_send
from file_read import read_file
import sys
import time

    

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

        print("\t1. Query")
        print("\t2. Exit")
        print("")
        choice = input("> ").strip()

        
        if choice == "1":
            #Adding code here
            print("Please enter the path of the file you want to read:")
            file_path = input()
            print("Please enter one IP part of delib:")
            user_ip = input()

            read_file(file_path, public_ip, 8000, user_ip, 8000)

   
            
        elif choice == "2":
            print("Exiting...")
            time.sleep(2)
            sys.exit()
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