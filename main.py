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

            # Start client program in seperate window
            arguments = "client.py"
            
            system = platform.system()

            if system == "Linux":
                terminal_command = ["x-terminal-emulator", "-e", sys.executable, arguments]
            elif system == "Darwin": 
                terminal_command = ["open", "-a", "Terminal.app", sys.executable, arguments]
            elif system == "Windows":
                terminal_command = ["start", "cmd", "/k", sys.executable, arguments]
            else:
                raise OSError(f"Unsupported operating system: {system}")
            
            if system == "Linux":
                subprocess.Popen(terminal_command, start_new_session=True)
            elif system == "Windows":
                subprocess.Popen(terminal_command, start_new_session=True, shell=True)

            # Start the server program in this window
            node.run()
            break
        
        if choice == "2":
            ip = input("Please enter one of the Node's IP address : ")
            node = Node(ip)

            # Start client program in seperate window
            arguments = "guest_client.py"
            
            system = platform.system()

            if system == "Linux":
                terminal_command = ["x-terminal-emulator", "-e", sys.executable, arguments]
            elif system == "Darwin": 
                terminal_command = ["open", "-a", "Terminal.app", sys.executable, arguments]
            elif system == "Windows":
                terminal_command = ["start", "cmd", "/k", sys.executable, arguments]
            else:
                raise OSError(f"Unsupported operating system: {system}")
            
            if system == "Linux":
                subprocess.Popen(terminal_command, start_new_session=True)
            elif system == "Windows":
                subprocess.Popen(terminal_command, start_new_session=True, shell=True)

            # Start the server program in this window
            node.run()
            break

        elif choice == "3":
            node = Node()
            
            # Start client program in seperate window
            arguments = "client.py"
            
            system = platform.system()

            if system == "Linux":
                terminal_command = ["x-terminal-emulator", "-e", sys.executable, arguments]
            elif system == "Darwin": 
                terminal_command = ["open", "-a", "Terminal.app", sys.executable, arguments]
            elif system == "Windows":
                terminal_command = ["start", "cmd", "/k", sys.executable, arguments]
            else:
                raise OSError(f"Unsupported operating system: {system}")
            
            if system == "Linux" or system == "Darwin":
                subprocess.Popen(terminal_command, start_new_session=True)
            elif system == "Windows":
                subprocess.Popen(terminal_command, start_new_session=True, shell=True)

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