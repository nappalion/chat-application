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

# Grab the host dynamically (changes for each PC)
# HOST = socket.gethostbyname(socket.gethostname())
HOST = 'localhost'
RECV_BUFFER = 4096
PORT = 12000

def server():
  # Create an internet type TCP socket
  serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  # Modifies the socket to make the address reusable
  serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

  serverSocket.bind((HOST, PORT))

  # Server can accept a maximum of 10 connections
  serverSocket.listen(10)

  socketList = [serverSocket]

  print(f'Server listening on {HOST}:{PORT}...')

  while True:
    read, write, error = select.select(socketList, [], socketList)

    for sock in read:
      # New client connection request has been received
      if sock == serverSocket:
        # Wait for incoming connections and return socket for communication and address when found
        clientSocket, clientAddress = serverSocket.accept()

        # Add the socket to the list of connected sockets so the server can send messages globally
        socketList.append(clientSocket)

        # Server prints which clients are connected to the console
        print(f'Client {clientAddress[0], clientAddress[1]} connected.')

        # Notify other connected clients of new socket connections
        sendMessage(serverSocket, clientSocket, "(%s, %s) entered the chatting room\n" % clientAddress, socketList)

        # Notify new client that they've been connected to the server
        clientSocket.send("Connected to the server!\n".encode("utf-8"))

      # New message from a client has been received
      else:
        try:
          data = sock.recv(RECV_BUFFER)

          if(data):
            sendMessage(serverSocket, sock, 'New Message: ' + str(data.decode("utf-8")) + '\n', socketList)
            print('Received message: ' + str(data.decode("utf-8")))
 
          else:
            if(sock in socketList):
              socketList.remove(sock)
            print("Client (%s, %s) disconnected\n" % clientAddress)
            sendMessage(serverSocket, sock, "Client (%s, %s) is offline\n" % clientAddress, socketList)
            break

        except:
          if(sock in socketList):
            socketList.remove(sock)
          print("Client (%s, %s) disconnected\n" % clientAddress)
          sendMessage(serverSocket, sock, "Client (%s, %s) is offline\n" % clientAddress, socketList)
          break

  serverSocket.close()

def sendMessage(serverSock, currSock, message, socketList):
  # Broadcast to all connected sockets except the current socket
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