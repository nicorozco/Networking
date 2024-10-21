from socket import *
# 1 create a "establishing/welcome" socket

serverPort = 12000

serverSocket = socket(AF_INET, SOCK_STREAM)

# 2 Bind Port number to Socket
serverSocket.bind(('',serverPort))

# 3 Listen for request from clients (.listen)
serverSocket.listen(1)

#Accept Connections (indefinelty)
while True:
        #4 Create a connection socket utilizing .accept()
        print("Waiting for connection .....")
        connectionSocket, addr = serverSocket.accept()
        
        print(f"Connected by {addr}")

        # 5 Recieve data through socket
        message = connectionSocket.recv(1024).decode()

        #modify data
        modifiedMessage = message.upper()

        #6 Send Data through the socket
        connectionSocket.send(modifiedMessage.encode())
        #7 close the socket connection
        connectionSocket.close()