from socket import *
# 1 create a socket 

serverPort = 12000
serverName = "127.0.0.1"

clientSocket = socket(AF_INET,SOCK_STREAM)

#2 Create a connection to server utilizing client socket
clientSocket.connect((serverName,serverPort))

#Get data from user
sentence = input('Input a lowecase sentence')

#3 Send Data through socket
clientSocket.send(sentence.encode())

#4 Recieve Data through socket
message = clientSocket.recv(1024).decode()

print('From Server: ', message)

#5 Close Connection of the socket
clientSocket.close()