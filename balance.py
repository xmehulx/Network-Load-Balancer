#!/usr/bin/python

import socket

# Create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a port
sock.bind(("10.0.0.254", 80))

# Listen for incoming connections
sock.listen(5)

while True:
    # Accept an incoming connection
    client_sock, client_addr = sock.accept()
    #D print("Received connection from", client_addr)

    # Choose a server to forward the connection to
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.connect(("10.0.0.1", 80))

    # Forward the connection
    #D server_sock.sendall(client_sock.recv(1024))
    while True:
        # Client > Server
        data = client_sock.recv(1024)
        if not data:
            break
        server_sock.sendall(data)

        # Server > Client
        data = server_sock.recv(1024)
        if not data:
            break
        client_sock.sendall(data)
    
    # Close the connections
    client_sock.close()
    server_sock.close()
