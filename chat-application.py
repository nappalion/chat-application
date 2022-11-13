import socket
import sys
import select

RECV_BUFFER = 4096
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
  serverSocket.listen(10)

  socketList.append(serverSocket)

  print("Server starting on port " + str(port))

  while True:
    read, write, error = select.select(socketList, [], [], 0)

    for sock in read:
      if sock == serverSocket:
        # do something

        sockOb, address = serverSocket.accept()
        socketList.append(sockOb)
        print("Client %s connected" % address)

        sendMessage(serverSocket, sockOb, "%s entered the chatting room\n" % address)

      else:

        try:
          data = sock.recv(RECV_BUFFER)

          if(data):
            sendMessage(serverSocket, sock, '\r' + str(sock.getpeername() + data))

          else:
            if(sock in socketList):
              socketList.remove(sock)

            sendMessage(serverSocket, sock, "Client %s is offline\n" % address)

        except:
          sendMessage(serverSocket, sock, "Client %s is offline\n" % address)
          continue

  serverSocket.close()

if __name__ == "__main__":
  sys.exit(server())