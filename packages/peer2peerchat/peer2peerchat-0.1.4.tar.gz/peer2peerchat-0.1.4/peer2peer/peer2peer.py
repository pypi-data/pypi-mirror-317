
import threading
import socket
import json
from pyperclip import copy, paste
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

snippets['mkfifo'] = r"""
// This side writes first, then reads
#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
 
int main()
{
    int fd;
 
    // FIFO file path
    char * myfifo = "/tmp/myfifo";
 
    // Creating the named file(FIFO)
    // mkfifo(<pathname>, <permission>)
    mkfifo(myfifo, 0666);
 
    char arr1[80], arr2[80];
    while (1)
    {
        // Open FIFO for write only
        fd = open(myfifo, O_WRONLY);
 
        // Take an input arr2ing from user.
        // 80 is maximum length
        fgets(arr2, 80, stdin);
 
        // Write the input arr2ing on FIFO
        // and close it
        write(fd, arr2, strlen(arr2)+1);
        close(fd);
 
        // Open FIFO for Read only
        fd = open(myfifo, O_RDONLY);
 
        // Read from FIFO
        read(fd, arr1, sizeof(arr1));
 
        // Print the read message
        printf("User2: %s\n", arr1);
        close(fd);
    }
    return 0;
}
"""


snippets['mkfifo_2'] = r"""
// This side reads first, then write
#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
 
int main()
{
    int fd1;
 
    // FIFO file path
    char * myfifo = "/tmp/myfifo";
 
    // Creating the named file(FIFO)
    // mkfifo(<pathname>,<permission>)
    mkfifo(myfifo, 0666);
 
    char str1[80], str2[80];
    while (1)
    {
        // First open in read only and read
        fd1 = open(myfifo,O_RDONLY);
        read(fd1, str1, 80);
 
        // Print the read string and close
        printf("User1: %s\n", str1);
        close(fd1);
 
        // Now open in write mode and write
        // string taken from user.
        fd1 = open(myfifo,O_WRONLY);
        fgets(str2, 80, stdin);
        write(fd1, str2, strlen(str2)+1);
        close(fd1);
    }
    return 0;
}
"""


snippets['admin_perm'] = r"""0777"""

snippets['thread_multiparam'] = r"""
#include <pthread.h>
#include <stdio.h>

/*sending multiple parameters to thread function*/
typedef struct thread_data {
   int a;
   int b;
   int result;

} thread_data;

void *myThread(void *arg)
{
   thread_data *tdata=(thread_data *)arg;

   int a=tdata->a;
   int b=tdata->b;
   int result=a+b;

   tdata->result=result;
   pthread_exit(NULL);
}

int main()
{
   pthread_t tid;
   thread_data tdata;

   tdata.a=10;
   tdata.b=32;

   pthread_create(&tid, NULL, myThread, (void *)&tdata);
   pthread_join(tid, NULL);

   printf("%d + %d = %d\n", tdata.a, tdata.b, tdata.result);   
}
"""

snippets['thread_array'] = r"""
#include <pthread.h>
#include <stdio.h>

/*sending array to thread function*/

void *myThread(void *arg)
{
   int *arr=(int *)arg;
   int sum=0;

   for(int i=0; i<5; i++)
   {
      sum+=arr[i];
   }

   pthread_exit((void *)sum);
}

int main()
{
   pthread_t tid;
   int arr[5]={1,2,3,4,5};
   int sum;

   pthread_create(&tid, NULL, myThread, (void *)arr);
   pthread_join(tid, (void **)&sum);

   printf("Sum of array elements: %d\n", sum);   
}
"""

snippets['thread_return'] = r"""
/*sending and recieving a char to the thread function*/

#include <pthread.h>
#include <stdio.h>

void *myThread(void *arg)
{
    char c = *(char *)arg;

    // return samme char after printing
    printf("Character: %c\n", c);

    // return c
    pthread_exit((void *)c);
}

int main()
{
    pthread_t tid;
    char c = 'A';

    char *ret;
    pthread_create(&tid, NULL, myThread, (void *)&c);
    pthread_join(tid, (void **)&c);

    printf("Returned Character: %c\n", c);

    return 0;
}
"""

snippets['semaphores'] = r"""
/*use semaphore to synchronize threads*/

// C program to demonstrate working of Semaphores 
#include <stdio.h> 
#include <pthread.h> 
#include <semaphore.h> 
#include <unistd.h> 

sem_t mutex; //declare global semaphore

void* thread(void* arg) 
{ 
	//wait 
	sem_wait(&mutex); 
	printf("\nEntered..\n"); 

	//critical section 
	sleep(4); 
	
	//signal 
	printf("\nJust Exiting...\n"); 
	sem_post(&mutex); 
} 


int main() 
{ 
	sem_init(&mutex, 0, 1); 
	pthread_t t1,t2; 
	pthread_create(&t1,NULL,thread,NULL); 
	sleep(2); 
	pthread_create(&t2,NULL,thread,NULL); 
	pthread_join(t1,NULL); 
	pthread_join(t2,NULL); 
	sem_destroy(&mutex); 
	return 0; 
} 
"""

snippets['semaphore_example'] = r"""
#include <iostream>
#include <semaphore.h>
#include <pthread.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string>

using namespace std;

int glb_index = 0;
int gbArr[100];
sem_t sem;

void *threadAdd(void *numToAdd)
{
    int num = *(int *)numToAdd;
    sem_wait(&sem);
    for (int i = glb_index; i < glb_index+10; i++)
    {
       gbArr[i] = num;
    }
    glb_index += 10;
    sem_post(&sem);
    pthread_exit(NULL);
}

int main()
{

    sem_init(&sem, 0, 1);
    pthread_t threads [10];

    for (int i = 0; i < 10; i++)
    {
        int *thread_id = new int(i);
        pthread_create(&threads[i], NULL, threadAdd, (void *)thread_id);
        pthread_join(threads[i], NULL);
    }

    for (int i = 0; i < 100; i++)
    {
        cout << gbArr[i] << " ";
    }

    cout << "Final Sum:";
    int sum = 0;
    for (int i = 0; i < 100; i++)
    {
        sum += gbArr[i];
    }

    cout << sum << endl;
}
"""

snippets['includes'] = r"""
#include <iostream>
#include <fstream>
#include <pthread.h>
#include <semaphore.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ipc.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/shm.h>
#include <sys/wait.h>
#include <unistd.h>
#include <fcntl.h>
#include <cctype>
#include <errno.h>
"""

snippets['shm'] = r"""
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/shm.h>
#include <sys/ipc.h>
#include <string.h>

#define SHM_SIZE 1024

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <file>\n", argv[0]);
        exit(1);
    }

    // Generate a unique key
    key_t key = ftok("shmfile", 65);

    // Create a shared memory segment
    int shmid = shmget(key, SHM_SIZE, 0666 | IPC_CREAT);
    if (shmid == -1) {
        perror("shmget");
        exit(1);
    }

    // Attach to the shared memory segment
    char *shmaddr = shmat(shmid, NULL, 0);
    if (shmaddr == (char *)(-1)) {
        perror("shmat");
        exit(1);
    }

    // Open the file and read data
    int fd = open(argv[1], O_RDONLY);
    if (fd == -1) {
        perror("open");
        exit(1);
    }

    // Read data from file
    char buffer[SHM_SIZE];
    int bytesRead = read(fd, buffer, sizeof(buffer) - 1);
    if (bytesRead == -1) {
        perror("read");
        exit(1);
    }
    buffer[bytesRead] = '\0';
    close(fd);

    // Write data to shared memory
    strncpy(shmaddr, buffer, SHM_SIZE);

    printf("Data written to shared memory: %s\n", buffer);

    // Detach from shared memory
    if (shmdt(shmaddr) == -1) {
        perror("shmdt");
        exit(1);
    }

    return 0;
}
"""


snippets['mmap'] = r"""
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>
#include <iostream>

int main(int argc, char *argv[]) {
    int fd = open(argv[1], O_RDONLY);
    if (fd == -1) {
        perror("open");
        return 1;
    }

    char *map = (char*)mmap(NULL, 100, PROT_READ, MAP_PRIVATE, fd,0);
    if (map == MAP_FAILED) {
        perror("mmap");
        return 1;
    }

    std::cout << "Contents of file: " << map << std::endl;

    if (munmap(map, 100) == -1) {
        perror("munmap");
        return 1;
    }

    close(fd);
    return 0;
}
"""

snippets['mmap_ex'] = r"""
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>
#include <iostream>
#include <cstring>

void replaceWordInFile(const char *fileName, const char *wordToReplace, const char *replacementWord) {
    int fd = open(fileName, O_RDWR);
    if (fd == -1) {
        perror("open");
        return;
    }

    size_t length = lseek(fd, 0, SEEK_END);
    char *map = (char*)mmap(NULL, length, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (map == MAP_FAILED) {
        perror("mmap");
        close(fd);
        return;
    }

    char *pos = map;
    size_t replaceLen = strlen(wordToReplace);
    size_t replacementLen = strlen(replacementWord);

    while ((pos = strstr(pos, wordToReplace)) != NULL) {
        memcpy(pos, replacementWord, replacementLen);
        pos += replaceLen;
    }

    if (munmap(map, length) == -1) {
        perror("munmap");
    }

    close(fd);
}

int main(int argc, char *argv[]) {
    if (argc != 4) {
        std::cerr << "Usage: " << argv[0] << " <file> <wordToReplace> <replacementWord>\n";
        return 1;
    }

    replaceWordInFile(argv[1], argv[2], argv[3]);
    return 0;
}
"""

snippets['mmap_ex2'] = r"""
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>
#include <iostream>
#include <pthread.h>
#include <cctype>

#define FILE_SIZE 100

void *replaceIntegers(void *arg) {
    char *start = (char*)arg;
    for (int i = 0; i < FILE_SIZE / 2; ++i) {
        if (isdigit(start[i])) {
            start[i] = ' ';
        }
    }
    return NULL;
}

void replaceIntegersInFile(const char *fileName) {
    int fd = open(fileName, O_RDWR);
    if (fd == -1) {
        perror("open");
        return;
    }

    char *map = (char*)mmap(NULL, FILE_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (map == MAP_FAILED) {
        perror("mmap");
        close(fd);
        return;
    }

    pthread_t t1, t2;
    pthread_create(&t1, NULL, replaceIntegers, map);
    pthread_create(&t2, NULL, replaceIntegers, map + (FILE_SIZE / 2));

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    if (munmap(map, FILE_SIZE) == -1) {
        perror("munmap");
    }

    close(fd);
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <file>\n";
        return 1;
    }

    replaceIntegersInFile(argv[1]);
    return 0;
}
"""

snippets['file_manaipulation'] = r"""
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

int main() {
    const char *filename = "example.txt";
    char buffer[100];
    
    // Open the file for reading and writing, create if it doesn't exist
    int fd = open(filename, O_RDWR | O_CREAT, 0644);
    if (fd == -1) {
        perror("open");
        exit(1);
    }

    // Write data to the file
    const char *data = "Hello, World!";
    ssize_t bytesWritten = write(fd, data, 13);
    if (bytesWritten == -1) {
        perror("write");
        close(fd);
        exit(1);
    }

    // Seek to the beginning of the file
    if (lseek(fd, 0, SEEK_SET) == -1) {
        perror("lseek");
        close(fd);
        exit(1);
    }

    // Read data from the file
    ssize_t bytesRead = read(fd, buffer, sizeof(buffer) - 1);
    if (bytesRead == -1) {
        perror("read");
        close(fd);
        exit(1);
    }
    buffer[bytesRead] = '\0'; // Null-terminate the string

    printf("Read from file: %s\n", buffer);

    // Close the file
    if (close(fd) == -1) {
        perror("close");
        exit(1);
    }

    return 0;
}
"""

if __name__ == '__main__':
    peer=Peer()

