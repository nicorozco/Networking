from socket import *
# 1 create server socket (IPv4,,Datagram for (UDP))
serverSocket = socket(AF_INET,SOCK_DGRAM)


# 2 Bind the socket to port number
serverPort = 12345
serverName = "127.0.0.1"

serverSocket.bind(('',serverPort))

# since this isn't UTP we dont have to listen/establish a connection beforehand
print("Waiting for connection from client")
# 3 Recieve Data from Client from socket, we utilize recvfrom giving us the message itself and address to where to send it
while True:
    message, addr = serverSocket.recvfrom(1028)

    print(message.decode())
    print(addr)

    # 4 Send Data to client utilzing the addr from the .recfrom method
    serverSocket.sendto(message,addr)

    #5 close connection 
