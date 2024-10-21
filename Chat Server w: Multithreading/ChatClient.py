import threading
from socket import *


#recieve message through client socket from other clients (function)
def recMessage(clientSocket):
    # indefinetly accept message
    while True:
        try:
            message = clientSocket.recv(1024).decode()
            #if there is a message from the socket
            if message:
                    #print it
                    print(message)
            else:
                    #stop
                break
        except:
                break

#Main 
def main():
   
   # Server information has to be known 
    serverPort = 12345
    serverName = "127.0.0.1"

    #create client socket
    clientSocket = socket(AF_INET,SOCK_STREAM)

    #connect socket to the server
    clientSocket.connect((serverName,serverPort))

    print("Connected to the server, start sending messages")

    #start a thread to listen for incoming message
    recieveThread = threading.Thread(target = recMessage, args = (clientSocket,))
    
    #starting thread 
    recieveThread.start()

    #start indefinetly getting input from user
    while True:
        message = input()
        #if user added something to message send it out the client socket  
        if message:
                clientSocket.send(message.encode())

if __name__ == "__main__":
    main()