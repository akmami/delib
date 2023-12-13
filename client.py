import requests
import os
import socket
from pathlib import Path
from decouple import config
import json
from file_send import file_send
from file_remove import remove
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
        print("\t1. Add Document")
        print("\t2. Delete Document")
        print("\t3. Query")
        print("\t4. Exit")
        print("")
        choice = input("> ").strip()

        if choice == "1":
            #Adding code here
            print("Please enter the path of the file you want to add:")
            file_path = input()
            print("Please enter one IP part of delib:")
            user_ip = input()

            if os.path.exists(file_path):
                try:
                    with open(file_path, 'rb') as file:
                        file_data = file.read()

                    file_send(file_path, public_ip, 8000, user_ip, 8000)
                except PermissionError:
                    print(f"Permission error: Unable to add '{file_path}'.")
                except Exception as e:
                    print(f"An error occurred: {e}")  
            else:
                print("This file does not exist!")



        elif choice == "2":
            #Adding code here
            print("Please enter the path of the file you want to delete:")
            file_path = input()
            print("Please enter one IP part of delib:")
            user_ip = input()

            if os.path.exists(file_path):
                try:
                    remove(file_path, public_ip, 8000, user_ip, 8000)
                except PermissionError:
                    print(f"Permission error: Unable to delete '{file_path}'.")
                except Exception as e:
                    print(f"An error occurred: {e}") 
            else:
                print("This file does not exist!")

        elif choice == "3":
            #Adding code here
            print("Please enter the path of the file you want to read:")
            file_path = input()
            print("Please enter one IP part of delib:")
            user_ip = input()

            read_file(file_path, public_ip, 8000, user_ip, 8000)

        elif choice == "4":
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