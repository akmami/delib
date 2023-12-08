from node import Node
import subprocess
import sys 

def main():
    print("Welcome to Online Library Catalog Stored in Decentralised Network (delib)")
    print("You can either request to join existing network or create your own one.")
    while True:
        print("Please specify your choice.")
        print("")
        print("\t1. Join")
        print("\t2. Create")
        print("")
        choice = input("> ")

        if choice == "1":
            ip = input("Please enter one of the Node's IP address : ")
            node = Node(ip)

            # Start client program in seperate window
            script_path = "client.py"
            if sys.platform.startswith('win'):
                command = ["start", "cmd", "/k", "python3", script_path]
            else:
                command = ["x-terminal-emulator", "-e", "python3", script_path]

            # Run the script in a separate window
            subprocess.run(command)

            # Start the server program in this window
            node.run()
            break

        elif choice == "2":
            node = Node()
            
            # Start client program in seperate window
            script_path = "client.py"
            if sys.platform.startswith('win'):
                command = ["start", "cmd", "/k", "python3", script_path]
            else:
                command = ["x-terminal-emulator", "-e", "python3", script_path]

            # Run the script in a separate window
            subprocess.run(command)
            
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