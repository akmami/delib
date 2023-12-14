from node import Node
import platform
import subprocess 
import sys



def main():
    print("Welcome to Online Library Catalog Stored in Decentralised Network (delib)")
    print("You can either request to join existing network or create your own one.")
    while True:
        print("Please specify your choice.")
        print("")
        print("\t1. Join as node")
        print("\t2. Join as guest")
        print("\t3. Create")
        print("")
        choice = input("> ")

        if choice == "1":
            ip = input("Please enter one of the Node's IP address : ")
            node = Node(ip)

            # Start the server program in this window
            node.run()
            break
        
        if choice == "2":
            ip = input("Please enter one of the Node's IP address : ")
            node = Node(ip)

            # Start the server program in this window
            node.run(authority=False)
            break

        elif choice == "3":
            node = Node()
            # Start the server program in this window
            node.run()
            break
        else:
            print("")
            print("Invalid argument provided. Please enter 1 or 2.")
            
        
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
# MARK: Main
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()