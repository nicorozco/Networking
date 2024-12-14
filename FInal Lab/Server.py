# Server Side of Client-Chat Assignment
# Small Group #
# Created by Nicolas Orozco and Javier Mojica-Hernandez

import socket
import argparse
import sys 
import re
clientCounter = 0 # counter in order to see which how many users registered 
client_information1=[]
client_information2=[]
#____ Functions _____

def validate_server(server): # Function validate the socket is between the allowed socket number range and ensure the ip is valid
    match = re.match(r"^(\d{1,3}\.){3}\d{1,3}:(\d+)$", server) # validating if the input was given correct and matching if the server ip is given correctly
    if not match:
        raise argparse.ArgumentTypeError(f"Invalid server format: {server}. Expected format <IP:PORT>.")
    ip, port = server.split(":") # Split the argument into IP and port
    port = int(port)  # Validate server port number
    if port < 1 or port > 65535:
        raise argparse.ArgumentTypeError(f"Invalid server format: '{server}'. Expected format is <IP>:<PORT>.")
    return server # if port and ip is correct we return the server value 


 

#Function to handle incoming connections, where the connectionSocket is the socket created from the server listening to connection and 
# the address of the client exctracted when a connection is established 
def handle_connection (connectionSocket,addr):
    global clientCounter,client_information1,client_information2

    print(f"Connection established with {addr} \n")

    message,client1Address = connectionSocket.recvfrom(1024) #we want recieved a message from the connection and we unpack that data 
    text_message = message.decode()
    #once a message arrives at the port, 
    # we have to strip the data and header from it 
    # by utilizing .splitlines() method to seperating the message into different lines 
    
    message_split = text_message.splitlines() # list with the client's information 
    
    if message_split[0] == "REGISTER":
        clientid = message_split[1].split(": ",1)[1]
        ip = client1Address
        port = message_split[3 ].split(": ",1)[1]
        
        if clientCounter == 0:  # the first index of the message split will contain the request type and we check it , header is REGISTER
          client_information1= [clientid,addr,port] 
          clientCounter += 1 
          print(f"Client Counter: {clientCounter}")
            #create regack message
          regack_msg = "REGACK\r\n"
          regack_msg+= f"{client_information1[0]}\r\n"
          regack_msg+= f"{addr}\r\n"
          regack_msg+= f"{client_information1[2]}\r\n"
          regack_msg+= "Status: Registed\r\n"
          regack_msg+= "\r\n"
          print(regack_msg)
          connectionSocket.send(regack_msg.encode())#send the regack to the connectionSocket
        #print(f"{clientid} from {ip}:{port}")

        elif clientCounter > 0: 
           clientCounter += 1 
           print("Registering more than one client")
           print(f"Client Counter: {clientCounter}")
           client_information2 = [clientid,ip,port] 
           regack_msg = "REGACK\r\n"
           regack_msg+= f"{client_information2[0]}\r\n"
           regack_msg+= f"{client_information2[1]}\r\n"
           regack_msg+= f"{client_information2[2]}\r\n"
           regack_msg+= "Status: Registed\r\n"
           regack_msg+= "\r\n"
           connectionSocket.send(regack_msg.encode())#send the regack to the connectionSocket
    
    if message_split[0] == "BRIDGE":
        #print("Inside of Bridge")
        #print(f"Client Counter: {clientCounter}")
        if clientCounter == 1: #If only 1 registed client
            #print("Sending empty bridge")
            BRIACK_msg = "BRIDGEACK\r\n" # send empty bridge ack message
            connectionSocket.send(BRIACK_msg.encode())
         
        
        elif clientCounter == 2: # if there is 2 clients,
            #print("Sending Client2 the information")            
            BRIACK_msg = "BRIDGEACK\r\n"
            BRIACK_msg += f"{client_information1[0]}\r\n"
            BRIACK_msg += f"{client_information1[1]}\r\n"
            BRIACK_msg += f"{client_information1[2]}\r\n"
           
            connectionSocket.send(BRIACK_msg.encode()) # sending the information to the client
            

    if message_split[0] == "QUIT": #Close the TCP Connection when the chat is finsihed 
        print("Tearing down chat connection")
        connectionSocket.close()

#_________________ Server Main _______________________________   

def main():
   # we need to map the client's 
# this section is for settigng up the server ____________________________
    parser = argparse.ArgumentParser(description="Arguments to Start up Server  Program")
    parser.add_argument("--port", type= int,required=True, help = "Specify the server port number ex/ 5555")
    parser.add_argument("--ip", type= str,required=True, help = "Specify the server IP ex/ 127.0.0.1")

    args = parser.parse_args() # condense 
    port = args.port   # first arggument will be the port 
    ip = args.ip     # second arguemtn will be the IP 



    serArg = f"{ip}:{port}" # format into IP:PORT format
    validate_server(serArg)  # use function to validate the server

    serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    serverSocket.bind((ip,port)) # should allow commincation to happen from multiple computers
    serverSocket.listen(2) # the number of connections are able to wait 

    
    try: 
        while True:
            print(f"Server listening on {ip}:{port}")
            clientSocket, clientAddress = serverSocket.accept()
            print(clientAddress)
            handle_connection(clientSocket, clientAddress)
    except KeyboardInterrupt:
        print("\n")
        print("closing Server")
    finally:
        serverSocket.close()

    


#___________________________________________________________________________________________


if __name__ == "__main__":
    main()
