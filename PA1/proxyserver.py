import sys
from socket import *

if len(sys.argv) <= 1:
    print("Missing server IP address")
    sys.exit(2)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind((sys.argv[1], 8888))
tcpSerSock.listen(100)

while True:
    print("Listening on port 8888...")
    tcpCliSock, addr = tcpSerSock.accept()
    print("Received a connection from: ", addr)

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

        tcpCliSock.send("HTTP/1.0 200 OK\r\n".encode())
        tcpCliSock.send("Content-Type:text/html\r\n".encode())

        for i in range(0, len(outputdata)):
            tcpCliSock.send(outputdata[i])

        print("Read from cache!")

    except IOError:
        if fileExist == "false":
            c = socket(AF_INET, SOCK_STREAM)
            hostn = filename.replace("www.", "", 1)
            print(hostn)

            try:
                c.connect((hostn, 80))
                print("Connected to ", hostn)

                request = "GET " + "http://" + filename + " HTTP/1.0\r\n\r\n"
                c.send(request.encode())

                buffer = c.recv(4096)
                tmpFile = open("./" + filename, "wb")

                while buffer:
                    tmpFile.write(buffer)
                    tcpCliSock.send(buffer)
                    buffer = c.recv(4096)

            except Exception as e:
                print("Error occurred: ", type(e).__name__, e)

        else:
            tcpCliSock.send("HTTP/1.0 404 sendErrorErrorError\r\n")
            tcpCliSock.send("Content-Type:text/html\r\n")
            tcpCliSock.send("\r\n".encode())

            for i in range(0, len(outputdata)):
                tcpCliSock.send(outputdata[i])

    tcpCliSock.close()

tcpSerSock.close()