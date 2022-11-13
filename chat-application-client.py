import sys
import socket
import select

def client():
    host = input("Host name: ")
    port = int(input("Port number: "))

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.settimeout(2)

    try:
        clientSocket.connect((host, port))
    except:
        print("Unable to connect.")
        sys.exit()

    print("Connected to host " + str(host) + ". Try sending a message.")
    msg = input("Message: ")
    while True:
        socketList = [clientSocket]

        read, write, error = select.select(socketList, [], [])

        for sock in read:
            if sock == clientSocket:
                data = sock.recv(4096)
                if not data:
                    print("Disconnected from server")
                    sys.exit()
                else:
                    print("from some user: " + str(data.decode()))
                    msg = input("Message: ")

            else:
                clientSocket.send(msg.encode())
            

if __name__ == "__main__":
    client()

