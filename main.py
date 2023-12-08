from node import Node
import platform
import subprocess 

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
            command = "python3 client.py"
            
            system = platform.system()

            if system == "Linux":
                terminal_command = ["x-terminal-emulator", "-e",  command]
            elif system == "Darwin": 
                terminal_command = ["open", "-a", "Terminal.app", command]
            elif system == "Windows":
                terminal_command = ["start", "cmd", "/c", command]
            else:
                raise OSError(f"Unsupported operating system: {system}")
            
            subprocess.Popen(terminal_command, start_new_session=True)

            # Start the server program in this window
            node.run()
            break

        elif choice == "2":
            node = Node()
            
            # Start client program in seperate window
            command = "python3 client.py"
            
            system = platform.system()

            if system == "Linux":
                terminal_command = ["x-terminal-emulator", "-e",  command]
            elif system == "Darwin": 
                terminal_command = ["open", "-a", "Terminal.app", command]
            elif system == "Windows":
                terminal_command = ["start", "cmd", "/c", command]
            else:
                raise OSError(f"Unsupported operating system: {system}")
            
            subprocess.Popen(terminal_command, start_new_session=True)
            
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