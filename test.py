from threads import Thread
from node import Node
from time import sleep


localhost = "localhost"
port = 8001

node1 = Node(ip=localhost, port=port, ips=[8001, 8002, 8003])
node2 = Node(ip=localhost, port=port+1, ips=[8001, 8002, 8003])
node3 = Node(ip=localhost, port=port+2, ips=[8001, 8002, 8003])

thread1 = Thread(thread_name="node1", thread_ID=1, node=node1)
thread2 = Thread(thread_name="node2", thread_ID=2, node=node2)
thread3 = Thread(thread_name="node3", thread_ID=3, node=node3)

thread1.start()
thread2.start()
thread3.start()

thread1.join()
thread2.join()
thread3.join()