'''
Chatterbox Client-Server Application - Client  Code
CS3800

Members:
Richard Medina
Napoleon Torrico
Michael Holzer
'''

import socket

RECV_BUFFER = 4096

def client():
    HOST = 'localhost' #input("Host name: ")
    PORT = 12000 #int(input("Port number: "))

    # Create the TCP client socket and connect to the server
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((HOST, PORT))

    # Client socket in non-blocking mode to keep the code running (won't stop to wait)
    clientSocket.setblocking(False)

    # Send the username to the server
    username = input("Username: ")
    clientSocket.send(username.encode("utf-8"))

    while True:
        # Send current client's messages
        message = input("Me: ")
        if message:
            clientSocket.send(message.encode("utf-8"))
        
        # Wait for any incoming messages from the server 
        # (either server or client messages)
        try:
            while True:
                message = clientSocket.recv(RECV_BUFFER).decode("utf-8")
                print(f"{message}")

        except:
            # No messages
            pass
            

                
            

if __name__ == "__main__":
    client()

