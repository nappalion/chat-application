'''
Chatterbox Client-Server Application - Server Code
CS3800

Members:
Richard Medina
Napoleon Torrico
Michael Holzer
'''

import socket
import select

# Code to grab the host dynamically (changes for each PC):
# HOST = socket.gethostbyname(socket.gethostname())

# Chat room runs locally and on a port that's not taken
HOST = 'localhost'
PORT = 12000

RECV_BUFFER = 4096

# Server keeps track of all the sockets that are connected
socketList = []

# Dictionary to hold the username for each client socket
clients = {}

def server():
  global socketList, clients

  # Create an internet type TCP socket
  serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  # Modifies the socket to make the address reusable
  serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

  serverSocket.bind((HOST, PORT))

  # Server listens for new connections
  serverSocket.listen(10)

  socketList = [serverSocket]

  print(f'Server listening on {HOST}:{PORT}...')

  while True:
    # Get a list of the sockets that are ready to read
    read, write, error = select.select(socketList, [], socketList)

    for sock in read:
      # New client connection request has been received
      if sock == serverSocket:
        # Wait for incoming connections and return socket for communication and address when found
        clientSocket, clientAddress = serverSocket.accept()

        # Add the socket to the list of connected sockets so the client can receive messages from the server/other clients
        socketList.append(clientSocket)

        # When the client connects, wait for their username to be sent
        username = clientSocket.recv(RECV_BUFFER)

        # If they didn't send a username then they disconnected, so remove the current socket
        if username is False:
          socketList.remove(clientSocket)
          continue

        # Add the username to the dictionary
        clients[clientSocket] = username.decode("utf-8")

        # Server prints which clients are connected to the console
        print(f'Client {username.decode("utf-8")} at {clientAddress[0], clientAddress[1]} connected.')

        # Notify other connected clients of new socket connections
        sendMessage(serverSocket, clientSocket, f"Client {username.decode('utf-8')} at {clientAddress[0], clientAddress[1]} entered the chatting room.\n")

        # Notify new client that they've been connected to the server
        clientSocket.send("Connected to the server!\n".encode("utf-8"))

      # New message from a client has been received
      else:
        # If a client has sent a message, then we print it on the server and for each client
        try:
          data = sock.recv(RECV_BUFFER)

          if(data):
            sendMessage(serverSocket, sock, f'{clients[sock]}: ' + str(data) + '\n')
            print(f'{clients[sock]}: ' + str(data.decode("utf-8")))
 
          # If the data was invalid then the client has disconnected
          else:
            if(sock in socketList):
              socketList.remove(sock)
            print(f"Client {clients[sock]} at {clientAddress[0], clientAddress[1]} has disconnected.\n")
            sendMessage(serverSocket, sock, f"Client {clients[sock]} at {clientAddress[0], clientAddress[1]} is offline\n")
            break

        # If the data was invalid then the client has disconnected
        except:
          if(sock in socketList):
            socketList.remove(sock)
          print(f"Client {clients[sock]} at {clientAddress[0], clientAddress[1]} has disconnected.\n")
          sendMessage(serverSocket, sock, f"Client {clients[sock]} at {clientAddress[0], clientAddress[1]} is offline\n")
          break

  serverSocket.close()

# Broadcast to all connected sockets except the current and server sockets
def sendMessage(serverSock, currSock, message):
  global socketList, clients
  for socket in socketList:
    if socket != currSock and socket != serverSock:
      try:
        socket.send(message.encode("utf-8"))
      except:
        # If something went wrong with a socket, we close and remove it from the list
        socket.close()
        if(socket in socketList):
          socketList.remove(socket)

if __name__ == "__main__":
  server()