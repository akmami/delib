from node import Node


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
            break

        elif choice == "2":
            port = input("Please specify port (default 8000): ")
            while True:
                try:
                    port = int(port)
                except:
                    print("Invalid port number provided. Please enter integer.")
                    print("")
                
                node = Node(port=port, ips=[8001, 8002, 8003])
                node.run()
                break
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