import socket
import sys
import select

port = 80
socketList = []

def sendMessage(serverSocket, sock, message):
  for socket in socketList:
    if(socket != serverSocket and socket != sock):
      try:
        socket.send(message)
      except:
        socket.close()
        if(socket in socketList):
          socketList.remove(socket)


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
        sockOb, address = serverSocket.accept()
        socketList.append(sockOb)

      else:

        try:
          data = sock.recv(RECV_BUFFER)

          if(data):
            sendMessage(serverSocket, sock, '\r' + str(sock.getpeername() + data))
          else:
            if(sock in socketList):
              socketList.remove(sock)

        except:
          ''
        return