from socket import *
import sys

if len(sys.argv) <= 1:
    print("Usage: python proxyserver.py")
    sys.exit(2)

tcpSerSock = socket(AF_INET, SOCK_STREAM)

tcpSerSock.bind(("", 8888))
tcpSerSock.listen(5)

while True:
    print("Ready to serve...")
    tcpCliSock, addr = tcpSerSock.accept()
    print("Received a connection from:", addr)
    message = tcpCliSock.recv(1024).decode()
    print(message)

    print(message.split()[1])
    filename = message.split()[1].partition("/")[2]
    print(filename)
    fileExist = "false"
    filetouse = "/" + filename
    print(filetouse)

    try:
        f = open(filetouse[1:], "r", encoding='utf-8')
        outputdata = f.readlines()
        fileExist = "true"
        tcpCliSock.send(b"HTTP/1.0 200 OK\r\n")
        tcpCliSock.send(b"Content-Type:text/html\r\n")

        for i in range(0, len(outputdata)):
            tcpCliSock.send(outputdata[i].encode())

        print("Read from cache")

    except IOError:
        if fileExist == "false":
            c = socket(AF_INET, SOCK_STREAM)
            hostn = filename.replace("www.", "", 1)
            print(hostn)

            try:
                c.connect((hostn, 80))
                req = ("GET http://" + filename + " HTTP/1.0\r\n\r\n").encode()

                c.send(req)
                buff = c.recv(4096)

                tmpFile = open("./" + filename, "wb")
                tmpFile.write(buff)
                tmpFile.close()

            except Exception as e:
                print("Illegal request: ", e)

            c.close()
        else:
            tcpCliSock.send(b"HTTP/1.0 404 sendErrorErrorError\r\n")
            tcpCliSock.send(b"Content-Type:text/html\r\n")
            tcpCliSock.send(b"\r\n")

    # Close the client and the server sockets
    tcpCliSock.close()

tcpSerSock.close()