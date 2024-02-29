#import socket module
from socket import *

# Create a server socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a server socket
# Bind the socket to a specific address and port
serverPort = 6789
serverSocket.bind(('', serverPort))

# Listen for incoming connections
serverSocket.listen(1)
print('The server is ready to receive requests...')

while True:
    # Establish the connection
    connectionSocket, addr = serverSocket.accept()
    print('Accepted connection from:', addr)
    
    try:
        # Receive the HTTP request from the client
        message = connectionSocket.recv(1024).decode()
        print('Received request:\n', message)
        
        # Extract the filename from the request
        filename = message.split()[1]
        file_path = filename[1:]  # Remove the leading '/'
        
        try:
            # Open and read the requested file
            with open(file_path, 'rb') as file:
                outputdata = file.read()
                
            # Send the HTTP response header
            header = 'HTTP/1.1 200 OK\r\n\r\n'
            connectionSocket.send(header.encode())
            
            # Send the content of the requested file to the client
            connectionSocket.send(outputdata)
        except FileNotFoundError:
            # If the file is not found, send a "404 Not Found" response
            not_found_response = 'HTTP/1.1 404 Not Found\r\n\r\n'
            html_content = '<html><body><h1>404 Not Found</h1></body></html>'
            response = not_found_response + html_content
            connectionSocket.send(response.encode())
        
        # Close the connection
        connectionSocket.close()
    except Exception as e:
        print('Error handling request:', e)

# Close the server socket (Note: This will never be reached in this example)
serverSocket.close()