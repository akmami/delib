import threading


class Thread(threading.Thread): 
    def __init__(self, thread_name, thread_ID, node): 
        threading.Thread.__init__(self) 
        self.thread_name = thread_name 
        self.thread_ID = thread_ID 
        self.node = node
    

    def run(self): 
        print( str(self.thread_name) + " " + str(self.thread_ID) )

        self.node.run()