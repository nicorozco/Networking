# Client Side of Client-Chat Assignment
# Small Group #
# Created by Nicolas Orozco and Javier Mojica-Hernandez
#____ Libraries ____
import socket
import argparse
import sys 
import re

EMPTY_BRIDGE = True
client1Name ="" 
client1IP =""
client1Port = ""
client2Name =""

#____ Functions _____
# Function validate the socket is between the allowed socket number range and ensure the ip is valid
def validate_server(server):
    match = re.match(r"^(\d{1,3}\.){3}\d{1,3}:(\d+)$", server) # validating if the inpurt was given correct and matching if the server ip is given correctly
    if not match:
        raise argparse.ArgumentTypeError(f"Invalid server format: {server}. Expected format <IP:PORT>.")
    ip, port = server.split(":") # Split the argument into IP and port
    port = int(port)  # Validate server port number
    if port < 1 or port > 65535:
        raise argparse.ArgumentTypeError(f"Invalid server format: '{server}'. Expected format is <IP>:<PORT>.")
    return server # if port and ip is correct we return the server value 


def validate_port(port): # function to check if given client port is valid
    port = int(port)
    if port < 1 or port > 65535:  # Check if the port is not within the valid range for ports (1 to 65535)
        raise argparse.ArgumentTypeError(f"Invalid port: {port}. Must be between 1 and 65535.") #raise error if not 
    return port


def register_message(clientID, ip, port):
    # Define headers in a dictionary
    headers = {
        "clientID": clientID,
        "IP": ip,
        "Port": port
    }

    # Start constructing the message with the request line
    message = "REGISTER\r\n"

    # Dynamically add each header as a name-value pair
    for key, value in headers.items():
        message += f"{key}: {value}\r\n"

    # Add a blank line after the headers
    message += "\r\n"

    return message

# Create arge parse object to pass objects to
parser = argparse.ArgumentParser(description="Arguments to Start up Client Program")

# Adding arguments to the parses object of clientID, clientPort and server information 
parser.add_argument("--id", type=str,required= True, help = "Add the clientID")
parser.add_argument("--port", type=validate_port,required=True, help = "Add the clien port number")
parser.add_argument("--server", type= validate_server,required=True, help = "Specify the server IP and port in the format <IP:PORT>. Example: 127.0.0.1:8080")


args = parser.parse_args()

server = args.server
ip, port = server.split(":")
port_int = int(port)

while (True):

    line = (sys.stdin.readline(1024).strip()) #Get input (get input from the stdin)  
    if line == "/id": #Return id of the user
        print("UserID: ", args.id)
    elif line == '/register':
        try:
            clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # Create a client socket (IPv4 and TCP)
            try:
                clientSocket.connect((ip, port_int))  # Connect the socket to the server
                try:
                   
                    register = register_message(args.id, ip, args.port)  # Create a message with the client information
                    clientSocket.send(register.encode())  # Send the message to the server (encode the data to bytes)
                  
                except socket.error as send_error:
                    print(f"Error while sending data: {send_error}")
                finally:
                    clientSocket.close()  # Ensure the socket is closed
            except socket.error as connect_error:
                print(f"Error while connecting to the server: {connect_error}")
        except socket.error as socket_creation_error:
            print(f"Error while creating the socket: {socket_creation_error}")
    elif line == "/bridge": 
        clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        clientSocket.connect((ip, port_int))
       
        # Given inputs
        bridge_request = "BRIDGE\r\n"
        
        header1 = {"clientID": args.id}  # Assuming args.id is defined elsewhere in the code
    
        # Convert header1 dictionary to a string (you could format it in any way you like)
        header1_str = f"clientID:{header1['clientID']}\r\n"

        # Combine everything into the final message
        brd_msg = bridge_request + header1_str 
        clientSocket.send(brd_msg.encode()) #send info message to server
        
        try:
            clientInfoServ = clientSocket.recv(1040).decode() # recieve information from the server
            if clientInfoServ:
                chatInfo = clientInfoServ.splitlines()#extract the information and store the client name as the global variable 
                if chatInfo:
                    #print(chatInfo)
                    if len(chatInfo) > 2: #means we have another client
                        EMPTY_BRIDGE = False # set the variable to false
                        client1Name = chatInfo[1] #set the information
                        client1IP = chatInfo[2][0]
                        print(chatInfo[2])
                        client1Port = int(chatInfo[3])
                    else: # means there was no other client and we go into wait mode
                        print(f"{args.id}, IN WAIT MODE")
                        client1Socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)# create client 1 socket                     
                        client1Socket.bind(('',8081)) # Bind Client 1 socket to port 8080
                        client1Socket.listen(1) #put client1 on listening mode    
                        connectionSocket, addr = client1Socket.accept() #once we get a connection we create a socket for the chat connection
                    
                        chatMsg = connectionSocket.recv(1040).decode() #recieve information from our socket (Initial Message Request)
                        chatMsgInfo = chatMsg.splitlines() #split the information given from the socket to extract wanted information
                        print(f"Incoming message from {chatMsgInfo[2]} {addr}") #print chat request message with client 2 information
                      
                        if chatMsgInfo:
                            print(f">{chatMsgInfo[2]} {chatMsgInfo[1]}") #we print the intial message sent by client 2 
                            if chatMsgInfo[0] == "CHAT": # if the message is of type request and the information is valid, we print out the message and enter chat mode
                                if chatMsgInfo[1].lower() == "/quit": #if the intial contents of the chat message is quit
                                    sys.stdout.write("Ending Chat")
                                    connectionSocket.close() 
                                else: #Enter Chatting Mode 
                                    state = 1
                                    print(f"{args.id}, IN CHAT MODE")
                                    while True: 
                                        if state == 1: #Writing State
                                            message_request = "CHAT\r\n" # Create a request message with Chat Message Format
                                            chat_data = sys.stdin.readline().strip()  # recieved data from the terminal
                                            valid_message = message_request.isprintable()
                                            message_request+= f"{chat_data}\r\n" #add the data to the message
                                            if valid_message:
                                                connectionSocket.send(message_request.encode())
                                                state = 0
                                                print(chat_data)
                                            if chat_data.lower() == "/quit":  #if the user puts in quit, we break the state of chatting
                                                sys.stdout.write("Ending Chat")
                                                clientSocket.close() #close client connection before exiting
                                                break 
                    
                                        #________Reading State_________________
                                        elif state == 0:
                                            #print("Client 1 Reading State")
                                            incoming_message = connectionSocket.recv(1040).decode() #we recieve messages from the socket
                                            inc_msg1 = incoming_message.splitlines()
                                            if incoming_message.strip().lower() == "/quit": # if peer 1 sends a quit message, client 2 exits the while loop
                                                sys.stdout.write("Peer has ended the chat\n")
                                                connectionSocket.close() # close socket
                                                break 
                                            elif incoming_message:
                                                print(f">{chatMsgInfo[2]} {inc_msg1[1]}")
                                                state = 1 #once we print the message from client 1, we go into w
        except socket.error: # if error happens in "try" then should print out error
            print("Socket error during communication")
            clientSocket.close() # close the connection
    elif line == "/chat" and EMPTY_BRIDGE == False: 

        client2socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client2socket.connect(("127.0.0.0",8081)) #need tpo get this information

       
        #print("Connected to client 1")
        message_request = "CHAT\r\n" # Create a request message with Chat Message Format
        chat_data = sys.stdin.readline().strip()  # recieved data from the terminal
        client_name = args.id
        message_request+= f"{chat_data}\r\n" #add the data to the message
        message_request+= f"{client_name}\r\n"
        client2socket.send(message_request.encode())
        state = 0
        
        print(f"{args.id}, IN CHAT MODE")
        while True: 
            if state == 1: #Writing State
                #print("Client 2 Writing State")
                message_request = "CHAT\r\n" # Create a request message with Chat Message Format
                chat_data = sys.stdin.readline().strip()  # recieved data from the terminal
                message_request+= chat_data #add the data to the message
                valid_message = chat_data.isprintable()

                if valid_message:
                    client2socket.send(message_request.encode()) #send message to Client 1
                    state = 0 # once we send the message, we set the state to 0 or reading state

                if chat_data.lower() == "/quit":  #if the user puts in quit, we break the state of chatting
                    sys.stdout.write("Ending Chat")
                    client2socket.close() #close client connection before exiting
                    break 
          
            #________Reading State_________________
            elif state == 0:
                #print("Client 2 Reading State")
                incoming_message = client2socket.recv(1040).decode() #we recieve messages from the socket
                inc_msg = incoming_message.splitlines()
                if incoming_message.strip().lower() == "/quit": # if peer 1 sends a quit message, client 2 exits the while loop
                    sys.stdout.write("Peer has ended the chat\n")
                    client2socket.close() # close socket
                    break 
                elif incoming_message:
                    print(f">{client1Name} {inc_msg[1]}")
                    state = 1 #once we print the message from client 1, we go into writing state  
    elif KeyboardInterrupt or line == "/quit": #if ctrl + c is hit or client inputs /quit into the terminal -> program terminates  
        sys.exit()       
    else:       
        sys.stderr.write("Command not Found!")#show an error message for wrong input  

sys.stdout.write("Program terminated") 
sys.exit()#Terminate program

'''                    
                        except socket.error as e:
                            print(f"Socket error during bind() or listen(): {e}")
                            client1Socket.close()
                        finally:
                            clientSocket.close()
                            print('closing at last port')
    '''             
