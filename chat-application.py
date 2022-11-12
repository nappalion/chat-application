import socket
import sys
import select

port = 80
socketList = []

def server():

  serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  serverSocket.bind(('', port))
  socket.listen(1)

  socketList.append(serverSocket)

  while True:
    read, write, error = select.select(socketList, [], [], 0)

    for sock in read:
      if sock == serverSocket:
        # do something
        return