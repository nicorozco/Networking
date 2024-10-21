import threading
from socket import *
# a chat server very similar to the previous examples of simple client and server
# the only difference is both server and client need to handle multiple messages/clients being connected
# this where we utililize threading

## Basic Chat Server Functions ##  

#list of clients
clients = []

#1 Accept multiple client connections
def handleClient(clientSocket,clientAddress):
    while True:
        try:
            # Recieve messages from client
            message = clientSocket.recv(1024)
            #brodcast that message to all other clients
            #if we there is a message recieved brodcast it to the other connected clients
            if message:
                brodcast(f"{clientAddress}: {message}",clientSocket)
            else:
                # if no message is recieved, remove the client
                removeClient(clientSocket)
                break
        except:
            #in case of error remove the client
            removeClient(clientSocket)
            break

#3 Brodcast messages to all connected clients (Function)
def brodcast(message,clientSocket):
    # for all the clients in the client list
    for client in clients:
        # if the client is not equal to the current clientSocket (meaning not itself)
        if client != clientSocket:
            try:
                #send the message to the client through the socket 

                client.send(message)
                #else remove the client to not take space in the server
            except:
                removeClient(client)

# 3 Remove the client from the list of clients
def removeClient(clientSocket):
    #if the client socket is in the list
    if clientSocket in clients:
    #remove it from the list
        clients.remove(clientSocket)
    #close that connection
        clientSocket.close()

#Main 
def main():
#1 created for server to lsiten for connections socket
    serverSocket = socket(AF_INET,SOCK_STREAM)
    print("Server is active ")
    #2 bind socket
    serverPort = 12345
    serverSocket.bind(('',serverPort))
    
    # listen for communication (handshake)
    serverSocket.listen(2)
   
    #indefinetly accept connections
    while True:
        
        #accept client connections
        clientSocket, clientAddress = serverSocket.accept()
        print(f"New connection from {clientAddress}")
        
        # Add the client to the list of clients with the socket information 
        clients.append(clientSocket)

        #create a new thread for client
        clientThread = threading.Thread(target = handleClient, args = (clientSocket, clientAddress))
        clientThread.start()

if __name__ == "__main__":
    main()