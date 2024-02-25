import socket
import os

def handle_request(client_socket):
    # Receive the request from the client
    request = client_socket.recv(1024).decode()
    print("Request:")
    print(request)
    
    # Extract the filename from the request
    filename = request.split()[1]
    if filename == '/':
        filename = '/index.html'
    
    # Load the file content
    try:
        with open('.' + filename, 'rb') as file:
            content = file.read()
        response_headers = 'HTTP/1.1 200 OK\n\n'
        response_body = content
    except FileNotFoundError:
        response_headers = 'HTTP/1.1 404 Not Found\n\n'
        response_body = b'<html><body><h1>404 Not Found</h1></body></html>'
    
    # Send the response to the client
    response = response_headers.encode() + response_body
    client_socket.send(response)
    
    # Close the connection
    client_socket.close()

def main():
    # Create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to a host and port
    server_socket.bind(('127.0.0.1', 6789))
    
    # Listen for incoming connections
    server_socket.listen(1)
    print("Server is listening on port 6789...")
    
    while True:
        # Accept a new connection
        client_socket, client_address = server_socket.accept()
        print("Connection from:", client_address)
        
        # Handle the client's request
        handle_request(client_socket)

if __name__ == "__main__":
    main()
