
import threading
import socket
import json
from pyperclip import copy,paste

import os

"""
For clipboard:
On Linux, install xclip, xsel, or wl-clipboard (for "wayland" sessions) via package manager.
For example, in Debian:
    sudo apt-get install xclip
    sudo apt-get install xsel
    sudo apt-get install wl-clipboard
"""
try:
    os.system('title g++')
except Exception as e:
    print('Error occured while setting title: ', e)
    pass

def get_clipboard():
    try:
        return paste()
    except Exception as e:
        print("Clipboard paste failed: ", e)
        return None
    
def set_clipboard(data):
    try:
        copy(data)
    except Exception as e:
        print("Clipboard copy failed: ", e)

class MesssageType:
    JOIN = 1
    LEAVE = 2
    TEXT = 3
    FILE = 4
    PARTIAL_FILE = 5
    END_FILE = 6


snippets = {
    # keys should be in lowercase
}


class Message:
    def __init__(self, sender, content, message_type: MesssageType,file_name=None,seq=0) -> None:
        self.sender = sender
        self.content = content
        self.message_type = message_type
        self.file_name = file_name
        self.seq = seq

    def __str__(self) -> str:
        return f'{self.sender} - {self.content}'

    def __repr__(self) -> str:
        return f'{self.sender} - {self.content}'

    def to_json(self):
        return json.dumps({
            'sender': self.sender,
            'content': self.content,
            'message_type': self.message_type,
            'file_name': self.file_name,
            'seq': self.seq
        })

    @staticmethod
    def from_json(data):
        data = json.loads(data)
        return Message(data['sender'], data['content'], data['message_type'], data.get('file_name', None), data.get('seq', 0))

class Peer:
    def __init__(self, host = '0.0.0.0', port = 12345) -> None:
        self.peerlist = dict()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.port = port
        self.server.bind((host, self.port))
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # Increase the send buffer size
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536)
        
        # Increase the receive buffer size
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
        self.Sender_thread = threading.Thread(target=self.Sender,daemon=True)
        self.name = input('Enter your name: ')
        self.send_data(self.name, MesssageType.JOIN)
        self.run = True
        #Get address of the peer
        self.ip = socket.gethostbyname(socket.gethostname())
        print(f'Your IP Address is: {self.ip}')
        self.Sender_thread.start()
        self.listen()

    def Sender(self):
        while self.run:
            try:
                msg = input(':> ')
            except:
                print('Error occured while sending message')
                self.run = False
                break
            if msg == 'exit':
                self.send_data(self.name, MesssageType.LEAVE)
                self.server.close()
                break
            if msg == 'list':
                print(self.peerlist)
            elif msg in ['paste', 'p']:
                data = get_clipboard()
                if data:
                    self.send_data(data, MesssageType.TEXT)
            elif msg == 'cls':
                os.system('cls')
            elif msg in ['snippets', 's']:
                snippet_indexing = {i: key for i, key in enumerate(snippets.keys())}
                for i, key in snippet_indexing.items():
                    print(f'{i}. {key}')
                try:
                    required_snippet = int(input('Enter the snippet number: '))
                except:
                    print('Invalid input')
                    continue
                try:
                    snippet = snippets[snippet_indexing[required_snippet]]
                    print(snippet)
                except:
                    print('Invalid snippet number')

            elif msg.startswith('file'):
                filename = msg.split(' ')[1]
                self.send_data(filename, MesssageType.FILE)
            elif msg in ('help', 'h'):
                print("""
Commands:
1. list: List all the peers
2. paste - p: Send clipboard data
3. cls: Clear the screen
4. snippets - s: List all the snippets
5. file <filename>: Send file (alpha)
                """
                )
            else:
                self.send_data(msg, MesssageType.TEXT)
            


    def listen(self):
        file_data = dict()
        while self.run:
            try:
                data, addr = self.server.recvfrom(65536)
            except socket.error as e:
                print(e)
                break
            except KeyboardInterrupt:
                print('Keyboard Interrupt')
                self.run = False
                break
            message = Message.from_json(data)
            
            if addr[0] == self.ip:
                continue
            
            elif message.message_type == MesssageType.JOIN:
                name = message.content
                if addr not in self.peerlist:
                #self.server.sendto(f'join:{self.name}'.encode(), addr)
                    print(f'{name} joined the chat')
                    self.send_data(self.name, MesssageType.JOIN)
                    self.peerlist[addr] = name
            elif message.message_type == MesssageType.PARTIAL_FILE:
                if message.file_name not in file_data:
                    file_data[message.file_name] = dict()
                file_data[message.file_name][message.seq] = message.content
                
            elif message.message_type == MesssageType.END_FILE:
                keys = list(file_data[message.file_name].keys())
                keys.sort()
                with open(self.name+message.file_name, 'w') as file:
                    for key in keys:
                        file.write(file_data[message.file_name][key])
                    
                print(f'File {message.file_name} received')
            elif message.message_type == MesssageType.LEAVE:
                name = message.content
                print(f'{name} left the chat')
                self.peerlist.pop(addr)
            else:
                print(f"{message.sender}:{message.content}")

    def send_msg(self, data):
        self.server.sendto(data.encode(), ('255.255.255.255', 12345))
        

    def send_data(self, content, message_type: MesssageType):
        
        if message_type == MesssageType.TEXT:
            message = Message(self.name, content, message_type)
        elif message_type == MesssageType.FILE:
            with open(content, 'r') as file:
                seq = 0
                data = file.read(100)
                while data:
                    message = Message(self.name, data, MesssageType.PARTIAL_FILE, content,seq)
                    seq+=1
                    self.send_msg(message.to_json())
                    data = file.read(100)

                message = Message(self.name, '', MesssageType.END_FILE, content)
                
        else:
            message = Message(self.name, content, message_type)
        self.send_msg(message.to_json())
        
        
        



snippets['unnamed_pipe'] = r"""
#include <unistd.h>
#include <stdio.h>
#include <errno.h>

int main() {
  int ret_val;
  int pfd[2];
  char buff[32];
  char string1[] = "String for pipe I/O";

  ret_val = pipe(pfd); /* Create pipe */
  if (ret_val != 0) {
    /* Test for success */
    printf("Unable to create a pipe; errno=%d\n", errno);

    exit(1); /* Print error message and exit */
  }
  if (fork() == 0) {
    /* child program */
    close(pfd[0]); /* close the read end */
    ret_val = write(pfd[1], string1, strlen(string1)); /*Write to pipe*/
    if (ret_val != strlen(string1)) {
      printf("Write did not return expected value\n");
      exit(2); /* Print error message and exit */
    }
  } else {
    /* parent program */
    close(pfd[1]); /* close the write end of pipe */
    ret_val = read(pfd[0], buff, strlen(string1)); /* Read from pipe */
    if (ret_val != strlen(string1)) {
      printf("Read did not return expected value\n");
      exit(3); /* Print error message and exit */
    }
    printf("parent read %s from the child program\n", buff);
  }
  exit(0);
}
"""

snippets['tcp multithreaded'] = r"""
# server.py
import socket
import threading

def handle_client(client_socket, address):
   
    print(f"New connection from {address}")
    try:
        # Receive first number
        num1 = int(client_socket.recv(1024).decode())
        # Send acknowledgment
        client_socket.send("Received first number".encode())
        
        # Receive second number
        num2 = int(client_socket.recv(1024).decode())
        
        # Process the numbers (in this case, add them and multiply them)
        sum_result = num1 + num2
        product_result = num1 * num2
        
        # Send back the results
        response = f"Sum: {sum_result}, Product: {product_result}"
        client_socket.send(response.encode())
        
    except Exception as e:
        print(f"Error handling client {address}: {e}")
    finally:
        client_socket.close()
        print(f"Connection from {address} closed")

def start_server():
    
    # Create server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Allow port reuse
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind to localhost port 5555
    server_socket.bind(('localhost', 5555))
    
    # Listen for incoming connections
    server_socket.listen(5)
    print("Server is listening on localhost:5555")
    
    try:
        while True:
            # Accept new connection
            client_socket, address = server_socket.accept()
            
            # Create new thread to handle client
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, address)
            )
            client_thread.daemon = True
            client_thread.start()
            
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()

# client.py
import socket

def start_client():
   
    # Create client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to server
        client_socket.connect(('localhost', 5555))
        
        # Get first number from user
        num1 = input("Enter first number: ")
        client_socket.send(num1.encode())
        
        # Wait for server acknowledgment
        print(client_socket.recv(1024).decode())
        
        # Get second number from user
        num2 = input("Enter second number: ")
        client_socket.send(num2.encode())
        
        # Receive and print results
        result = client_socket.recv(1024).decode()
        print("Server response:", result)
        
    except ConnectionRefusedError:
        print("Could not connect to server. Is it running?")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()
"""

snippets['udp con'] = r"""
# server.py
import socket
import threading

def handle_client(server_socket):
   
    while True:
        try:
            # Receive data and client address
            data, client_address = server_socket.recvfrom(1024)
            
            # Convert received bytes to integer
            number = int(data.decode())
            
            # Store number for this client
            if client_address not in client_numbers:
                client_numbers[client_address] = []
            client_numbers[client_address].append(number)
            
            # Send acknowledgment back to client
            server_socket.sendto(b"Received", client_address)
            
            # If we have two numbers from this client, process and send result
            if len(client_numbers[client_address]) == 2:
                num1, num2 = client_numbers[client_address]
                result = f"Sum: {num1 + num2}, Product: {num1 * num2}"
                server_socket.sendto(result.encode(), client_address)
                del client_numbers[client_address]
                
        except Exception as e:
            print(f"Error handling client: {e}")

# Create UDP server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('localhost', 5555))
print("Server is listening on localhost:5555")

# Dictionary to store numbers from clients
client_numbers = {}

# Create and start client handling thread
client_thread = threading.Thread(target=handle_client, args=(server_socket,))
client_thread.daemon = True
client_thread.start()

try:
    # Keep main thread alive
    while True:
        pass
except KeyboardInterrupt:
    print("\nShutting down server...")
    server_socket.close()

# client.py
import socket
import time

# Create UDP client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 5555)

try:
    # Send first number
    num1 = input("Enter first number: ")
    client_socket.sendto(num1.encode(), server_address)
    
    # Wait for acknowledgment
    data, _ = client_socket.recvfrom(1024)
    print(f"Server response: {data.decode()}")
    
    # Send second number
    num2 = input("Enter second number: ")
    client_socket.sendto(num2.encode(), server_address)
    
    # Wait for acknowledgment
    data, _ = client_socket.recvfrom(1024)
    print(f"Server response: {data.decode()}")
    
    # Wait for result
    result, _ = client_socket.recvfrom(1024)
    print(f"Final result: {result.decode()}")
    
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    client_socket.close()
"""

snippets['filehandling'] = r"""
import os

# --- Basic File Handling Operations ---

# 1. Creating and Writing to a Simple Text File
filename_simple = "simple_data.txt"
data_simple = "This is some basic text data.\nIt has two lines."
with open(filename_simple, "w") as f:
    f.write(data_simple)
print(f"Created and wrote to '{filename_simple}'")

# 2. Reading a Simple Text File
with open(filename_simple, "r") as f:
    content_simple = f.read()
print(f"\nContent of '{filename_simple}':\n{content_simple}")

# 3. Appending to a Text File
append_data = "\nThis line was appended later."
with open(filename_simple, "a") as f:
    f.write(append_data)
print(f"\nAppended data to '{filename_simple}'")

# 4. Reading Line by Line
print(f"\nReading '{filename_simple}' line by line:")
with open(filename_simple, "r") as f:
    for line in f:
        print(line.strip())

# --- Saving Data for Manipulation (Focusing on Python Data Structures) ---

# 5. Saving a List to a Text File (One item per line)
filename_list = "my_list.txt"
my_list = ["apple", "banana", "cherry"]
with open(filename_list, "w") as f:
    for item in my_list:
        f.write(item + "\n")
print(f"\nSaved list to '{filename_list}'")

# 6. Loading a List from a Text File
loaded_list = []
with open(filename_list, "r") as f:
    for line in f:
        loaded_list.append(line.strip())
print(f"\nLoaded list from '{filename_list}': {loaded_list}")

# 7. Saving a Dictionary to a Text File (Simple Key-Value Pairs)
filename_dict_simple = "my_dict_simple.txt"
my_dict_simple = {"name": "John Doe", "age": 30, "city": "Anytown"}
with open(filename_dict_simple, "w") as f:
    for key, value in my_dict_simple.items():
        f.write(f"{key}:{value}\n")
print(f"\nSaved simple dictionary to '{filename_dict_simple}'")

# 8. Loading a Dictionary from a Simple Text File
loaded_dict_simple = {}
with open(filename_dict_simple, "r") as f:
    for line in f:
        key, value = line.strip().split(":", 1) # Split only at the first ':'
        loaded_dict_simple[key] = value
print(f"\nLoaded simple dictionary from '{filename_dict_simple}': {loaded_dict_simple}")

# 9. Saving a List of Dictionaries (More Complex Data)
filename_list_of_dicts = "my_data.txt"
my_data = [
    {"name": "Alice", "age": 25, "city": "New York"},
    {"name": "Bob", "age": 30, "city": "London"},
    {"name": "Charlie", "age": 22, "city": "Paris"}
]

# Saving as comma-separated values (CSV-like) with a header
with open(filename_list_of_dicts, "w") as f:
    header = ",".join(my_data[0].keys()) + "\n"
    f.write(header)
    for item in my_data:
        values = ",".join(str(value) for value in item.values()) + "\n"
        f.write(values)
print(f"\nSaved list of dictionaries to '{filename_list_of_dicts}' (CSV-like)")

# 10. Loading a List of Dictionaries from the File
loaded_data = []
with open(filename_list_of_dicts, "r") as f:
    header = [h.strip() for h in f.readline().strip().split(",")]
    for line in f:
        values = line.strip().split(",")
        if len(header) == len(values):
            loaded_data.append(dict(zip(header, values)))
print(f"\nLoaded list of dictionaries from '{filename_list_of_dicts}': {loaded_data}")

# --- Saving More Complex Data Structures for Manipulation ---

# 11. Saving a Dictionary with List Values
filename_dict_complex = "my_dict_complex.txt"
my_dict_complex = {
    "users": ["Alice", "Bob", "Charlie"],
    "ages": [25, 30, 22],
    "cities": ["New York", "London", "Paris"]
}

# Saving with a custom delimiter for list values
with open(filename_dict_complex, "w") as f:
    for key, value in my_dict_complex.items():
        f.write(f"{key}:" + "|".join(value) + "\n")
print(f"\nSaved dictionary with list values to '{filename_dict_complex}'")

# 12. Loading a Dictionary with List Values
loaded_dict_complex = {}
with open(filename_dict_complex, "r") as f:
    for line in f:
        key, value_str = line.strip().split(":", 1)
        loaded_dict_complex[key] = value_str.split("|")
print(f"\nLoaded dictionary with list values from '{filename_dict_complex}': {loaded_dict_complex}")

# 13. Saving Nested Dictionaries (Representing as Strings)
filename_nested_dict = "nested_dict.txt"
nested_data = {
    "user1": {"name": "Alice", "age": 25},
    "user2": {"name": "Bob", "age": 30}
}

# Saving by converting the inner dictionaries to strings
with open(filename_nested_dict, "w") as f:
    for key, value in nested_data.items():
        f.write(f"{key}:{str(value)}\n")
print(f"\nSaved nested dictionary to '{filename_nested_dict}' (string representation)")



"""

snippets['usefull functions'] = r"""
File Handling Functions

open(file, mode='r'): Opens a file. Returns a file object. Modes include 'r' (read), 'w' (write), 'a' (append), 'x' (create), 'b' (binary), 't' (text). Use with open(...) for automatic closing.

file.close(): Closes an open file object. Releases resources.

file.read(size=-1): Reads at most size characters from the file. Reads the entire file if size is negative or omitted.

file.readline(size=-1): Reads and returns one line from the file. Reads at most size characters.

file.readlines(hint=-1): Reads and returns a list of all lines from the file.

file.write(string): Writes the given string to the file.

file.writelines(iterable): Writes a sequence of strings to the file.

file.tell(): Returns the current file pointer position.

file.seek(offset, whence=0): Moves the file pointer. whence can be 0 (start), 1 (current), 2 (end).

os.path.exists(path): Checks if a file or directory exists at the given path.

os.remove(path): Deletes a file.

os.rename(src, dst): Renames a file from src to dst.

os.mkdir(path): Creates a new directory.

os.makedirs(path, exist_ok=False): Creates a directory and any missing parent directories.

os.rmdir(path): Removes an empty directory.

os.listdir(path='.'): Lists files and directories in the specified path.

os.chdir(path): Changes the current working directory.

os.getcwd(): Returns the current working directory.

String Functions

string.capitalize(): Returns a copy of the string with the first character capitalized and the rest lowercased.

string.casefold(): Returns a casefolded copy of the string, suitable for caseless comparisons. More aggressive than lowercasing.

string.center(width, fillchar=' '): Returns a centered string of length width padded with fillchar.

string.count(sub, start=0, end=len(string)): Counts the non-overlapping occurrences of sub in the string.

string.encode(encoding='utf-8', errors='strict'): Returns an encoded version of the string as a bytes object.

string.endswith(suffix, start=0, end=len(string)): Checks if the string ends with the specified suffix.

string.expandtabs(tabsize=8): Replaces tab characters with spaces.

string.find(sub, start=0, end=len(string)): Returns the lowest index where sub is found. Returns -1 if not found.

string.format(*args, **kwargs): Formats the string using the given arguments. Supports various formatting options.

string.format_map(mapping): Similar to format(), but takes a mapping object.

string.index(sub, start=0, end=len(string)): Similar to find(), but raises ValueError if sub is not found.

string.isalnum(): Checks if all characters in the string are alphanumeric.

string.isalpha(): Checks if all characters in the string are alphabetic.

string.isascii(): Checks if all characters in the string are ASCII characters.

string.isdecimal(): Checks if all characters in the string are decimal digits.

string.isdigit(): Checks if all characters in the string are digits.

string.isidentifier(): Checks if the string is a valid Python identifier.

string.islower(): Checks if all cased characters in the string are lowercase.

string.isnumeric(): Checks if all characters in the string are numeric.

string.isprintable(): Checks if all characters in the string are printable.

string.isspace(): Checks if all characters in the string are whitespace.

string.istitle(): Checks if the string is titlecased (each word starts with an uppercase character).

string.isupper(): Checks if all cased characters in the string are uppercase.

string.join(iterable): Concatenates the elements of an iterable into a single string with the string as a separator.

string.ljust(width, fillchar=' '): Returns a left-justified string of length width.

string.lower(): Returns a lowercased copy of the string.

string.lstrip([chars]): Removes leading characters from the string.

string.partition(sep): Splits the string at the first occurrence of sep.

string.replace(old, new, count=-1): Replaces occurrences of old with new.

string.rfind(sub, start=0, end=len(string)): Similar to find(), but searches from right to left.

string.rindex(sub, start=0, end=len(string)): Similar to index(), but searches from right to left.

string.rjust(width, fillchar=' '): Returns a right-justified string of length width.

string.rpartition(sep): Similar to partition(), but searches from right to left.

string.rsplit(sep=None, maxsplit=-1): Splits the string from right to left.

string.rstrip([chars]): Removes trailing characters from the string.

string.split(sep=None, maxsplit=-1): Splits the string into a list of substrings.

string.splitlines(keepends=False): Splits the string at line breaks.

string.startswith(prefix, start=0, end=len(string)): Checks if the string starts with the specified prefix.

string.strip([chars]): Removes leading and trailing characters from the string.

string.swapcase(): Returns a copy of the string with uppercase characters converted to lowercase and vice versa.

string.title(): Returns a titlecased version of the string.

string.translate(table): Translates characters using a translation table.

string.upper(): Returns an uppercased copy of the string.

string.zfill(width): Pads the string with zeros on the left.
"""

snippets['bgp'] = r"""
R1 have Subnet 10.0.0.0/8
R1(config)#router bgp 1
R1(config-router)#neighbor 172.16.0.2 remote-as 71
R1(config-router)#network 10.0.0.0 mask 255.0.0.0
R1(config-router)#exit
R1(config)#do write
Building configuration...[OK]
R1(config)#
Step 4: bgp configuration on Router R2:
R2(config)#router bgp 71
R2(config-router)#neighbor 172.16.0.1 remote-as 1
R2(config-router)#neighbor 172.14.0.2 remote-as 79
R2(config-router)#exit
R2(config)#do write
Building configuration...[OK]
R2(config)#
Step 5: bgp configuration on Router R3:
R3 have subnet 40.0.0.0/8
R3(config)#router bgp 79
R3(config-router)#neighbor 172.14.0.1 remote-as 71
R3(config-router)#network 40.0.0.0 mask 255.0.0.0
R3(config-router)#exit
R3(config)#do write
Building configuration...[OK
R3(config)#
Step 6: bgp configuration Testing and troubleshooting.
For bgp testing we will ping both pc and check the network communication.

Now I am on PC2:
PC>ipconfig
PC>ping 10.0.0.2
Step 7: check bgp route on router R1:
R1#show ip route
Step 8: Check whether bgp protocols configure or not on Routre R1:
R1#show ip protocols
Step 9: Show BGP Status
R1#show ip bgp summary
Show bgp neighbors status:
R1#show ip bgp neighbors
Similarly we check bgp route on Router R2:
R2#show ip route
R2#show ip protocols
Similarly check bgp route on Router R3:
R3#show ip route
R3#show ip protocols
"""
snippets['ospf'] = r"""
About OSPF

Open Shortest Path First(OSPF) is one of the dynamic routing protocols amongst others such as  EIGRP, BGP and and RIP. It is perhaps one of the most popular link state routing protocols. It is an open standard, so it can be run on routers from different vendors.

OSPF supports key features such as:

    IPv4 and IPv6 routing
    Classless routing
    Equal cost load balancing,
    Manual route summarization, etc.

OSPF has a default administrative distance of 110. It uses cost as the parameter for determining  route metric. It uses the multicast address of 224.0.0.5 and 224.0.0.6 for communication between OSPF-enabled neighbors

Routers running OSPF need to establish a neighbor relationship before exchanging routing updates. Each OSPF router runs the SFP algorithm to calculate the best routes and adds them to the routing table.

OSPF routers store routing and topology information in three tables.:

    Neighbor table-which stores information about OSPF neighbors.
    Topology table-stores topology structure of the network.
    Routing table-stores the best routes

OSPF neighborhood discovery

Routers running OSPF need to establish a neighbor relationship before exchanging routing updates. OSPF neighbors are dynamically discovered by sending Hello packets out each OSPF-enabled interface on a router. Hello packets are sent to the multicast address of 224.0.0.5.
OSPF areas

An area is simply a logical grouping of adjacent networks and routers. All routers in the same area have the same topology table and don't know about routers in other areas. The main benefits of using areas in an OSPF network are:

    Routing tables on the routers are reduced.
    Routing updates are reduced.

Each area in an OSPF network must be connected to the backbone area ( also known as area 0 ). All routers inside an area must have the same area ID .

A router that has interfaces in more than one area (for example area 0 and area 1) is known as an Area Border Router (ABR).  A router that connects an OSPF network to other routing networks (for example, to an EIGRP network) is called an Autonomous System Border Router (ASBR).

For now we'll configure basic OSPF. On to it then!

Basic  OSPF configuration.

1. Build the network topology.

basic ospf topology.PNG

2.Configure IP addresses on PCs and router interfaces.
Router 1

R1(config)#int fa 0/0
R1(config-if)#ip add 10.0.0.1 255.0.0.0
R1(config-if)#no shut
R1(config-if)#
R1(config-if)#int serial 0/0/0
R1(config-if)#ip add 20.0.0.1 255.0.0.0
R1(config-if)#no shut

Router 2

R2(config-if)#int fa0/0
R2(config-if)#ip add 30.0.0.1 255.0.0.0
R2(config-if)#no shut
R2(config-if)#
R2(config-if)#int serial0/0/0
R2(config-if)#ip address 20.0.0.2 255.0.0.0
R2(config-if)#no shut

Now do IP configurations for the PCs.

PC1  IP add 10.0.0.2  Subnet mask 255.0.0.0   Default gateway  10.0.0.1

PC2 IP add 30.0.0.2  Subnet mask 255.0.0.0    Default gateway   30.0.0.1

3. Configure OSPF on the routers.

The configuration is pretty simple and requires only two major steps:

1.  Enable OSPF on a router using the router ospf PROCESS_ID in the global configuration mode.

2.Define on which interfaces OSPF will run and what networks will be advertised using network IP_ADDRESS  WILCARD_MASK  AREA command in the OSPF configuration mode.

Note that the OSPF process ID doesn't have to be the same on all routers in order for the routers to establish a neighbor relationship, but the area parameter has to be the same on all neighboring routers in order for the routers to become neighbors.
Router 1

R1(config)#
R1(config)#router ospf 1
R1(config-router)#network 10.0.0.0  0.255.255.255  area 0
R1(config-router)#network 20.0.0.0  0.255.255.255  area 0

Router 2

R2(config)#
R2(config)#router ospf  2
R2(config-router)#network 20.0.0.0  0.255.255.255 area 0
R2(config-router)#network 30.0.0.0  0.255.255.255 area 0

As you can see from the above picture,we just need to enable OSPF on the routers which then advertise the networks directly connected to each of them.

Have in mind: The OSPF process IDs used for the two routers  have been made optionally different but their area  numbers must be the same.

4. Verify OSPF configuration

First, let's verify that the routers have established a neighbor relationship by typing the show ip ospf neighbor command on R1:

ospf neighborhood verification on R1.PNG

Next, to verify that R1 has learnt the route to 30.0.0.0/8 network, we'll use  show ip route ospf command on R1:

show ip ospf on R1.PNG

Note that the letter O indicates OSPF routes.

Lastly, verify connectivity. Ping PC2 from PC1. Ping should be successful.

PC1 ping to PC2.PNG

Other OSPF verification commands

    show ip ospf  neighbors detail

    show ip ospf database

    show ip ospf interface

All the best!

You may also like to read:"""




if __name__ == '__main__':
    peer=Peer()

