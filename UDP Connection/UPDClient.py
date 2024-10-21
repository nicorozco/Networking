from socket import *
# 1 create client socket
clientSocket = socket(AF_INET,SOCK_DGRAM)

# We dont create connection with the server, therefore we only send data 
message = input("Please enter a message")
# 2 Send data to specified server utilizng gethome and the port number along with the message
serverName = "127.0.0.1"
serverPort = 12345

clientSocket.sendto(message.encode(),(serverName,serverPort))

# 3 recieve data from the server
message, addr = clientSocket.recvfrom(2048)

print(message.decode())

# 4 close the connection 
print("Closing the connection")

clientSocket.close()