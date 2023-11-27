# delib

Default program parameters are defined in .env file. This file is supposed to store sensitive information related to the project but in our case, we used it as environmental variable storage.

## Installation

Please install required libraries before executing functions

```bash
pip3 install -r requirements.txt
```

## Local SETUP

As in the local setup, IP addresses will be same, requesting other nodes will be done on different according to PORT numbers. 

The other important point is that each node should be created on different terminal windows.

Please execute ``main.py`` function and select create new one for the first node. Please select 8001 for the PORT number.

Then, on another window, follow same steps but choose 8002 as PORT number.

For the last node, the PORT number will be 8003.

As nodes will be running on 3 different windows, open new one and call send file function as 

```bash
python3 send.py --filepath [file-to-send] --sender_ip 127.0.1.1 --sender_port 8002 --receiver_ip 127.0.1.1 --receiver_port 8003
```

This function will trigger node with PORT number 8002 to send given file to the node that is listening PORT number 8003.

