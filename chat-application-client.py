'''
Chatterbox Client-Server Application - Client  Code
CS3800

Members:
Richard Medina
Napoleon Torrico
Michael Holzer
'''

import sys
import socket

RECV_BUFFER = 4096

def client():
    HOST = 'localhost' #input("Host name: ")
    PORT = 12000 #int(input("Port number: "))

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    clientSocket.connect((HOST, PORT))

    clientSocket.setblocking(False)

    while True:
        message = input("Me: ")
        if message:
            clientSocket.send(message.encode("utf-8"))
        
        try:
            while True:
                message = clientSocket.recv(RECV_BUFFER).decode("utf-8")
                print(f"{message}")

        except:
            # No messages
            pass
            

                
            

if __name__ == "__main__":
    client()

