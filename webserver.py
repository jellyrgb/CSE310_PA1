from socket import *

serverSocket = socket(AF_INET, SOCK_STREAM)

serverPort = 6789
serverSocket.bind(('', serverPort))

serverSocket.listen(1)
print('The server is ready to receive requests...')

while True:
    connectionSocket, addr = serverSocket.accept()
    print('Accepted connection from:', addr)
    
    try:
        message = connectionSocket.recv(1024).decode()
        print('Received request:\n', message)
        
        filename = message.split()[1]
        file_path = filename[1:] 
        
        try:
            with open(file_path, 'rb') as file:
                outputdata = file.read()
                
            header = 'HTTP/1.1 200 OK\r\n\r\n'
            connectionSocket.send(header.encode())
            
            connectionSocket.send(outputdata)
        except FileNotFoundError:
            not_found_response = 'HTTP/1.1 404 Not Found\r\n\r\n'
            html_content = '<html><body><h1>404 Not Found</h1></body></html>'
            response = not_found_response + html_content
            connectionSocket.send(response.encode())
        
        connectionSocket.close()
    except Exception as e:
        print('Error handling request:', e)

serverSocket.close()