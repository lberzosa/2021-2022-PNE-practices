import socket

# Configure the Server's IP and PORT
PORT = 8081
IP = "192.168.1.36"
MAX_OPEN_REQUESTS = 5

# Counting the number of connections
number_con = 0

# create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    serversocket.bind((IP, PORT))
    # become a server socket
    # MAX_OPEN_REQUESTS connect requests before refusing outside connections
    serversocket.listen(MAX_OPEN_REQUESTS)

    while True:
        # accept connections from outside
        print("Waiting for connections at {}, {} ".format(IP, PORT))
        (clientsocket, address) = serversocket.accept()

        # Another connection!e
        number_con += 1

        # Print the conection number
        print("CONNECTION: {}. From the IP: {}".format(number_con, address))

        # Read the message from the client, if any
        msg = clientsocket.recv(2048).decode("utf-8")
        print("Message from client: {}".format(msg))

        # Send the messag
        message = "Hello from the teacher's server"
        send_bytes = str.encode(message)
        # We must write bytes, not a string
        clientsocket.send(send_bytes)
        clientsocket.close()

except socket.error:
    print("Problems using port {}. Do you have permission?".format(PORT))

except KeyboardInterrupt:
    print("Server stopped by the user")
    serversocket.close()
It will wait for the clients to connect. Once a client is connected, It will print the message given by the client (if any) and response with a greeting message

Sending messages to the server from the command line
Once the Teacher's server is running, we will use the commands printf and nc for sending messages to it. Execute the following command from your LAB computer. Change the IP and Port according to the Teacher's specification:

printf "Testing!!! :-)" | nc 192.168.124.179 8080
You will see the server's response printed on your console:



In the Server's console, you will see your message:



Client-1: Creating the socket and sending a message to the server
Let's learn how to send messages from our python programs. We will assume that there is already a server running and we will connect to it and send them messages

For doing that, we need sockets. For creating a socket we will use the system module socket

Create the client.py file with this code (inside the Session-08 folder)

import socket

# SERVER IP, PORT
# Write here the correct parameter for connecting to the
# Teacher's server
PORT = 8080
IP = "192.168.124.179"


# First, create the socket
# We will always use this parameters: AF_INET y SOCK_STREAM
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# establish the connection to the Server (IP, PORT)
s.connect((IP, PORT))

# Send data. No strings can be send, only bytes
# It necesary to encode the string into bytes
s.send(str.encode("HELLO FROM THE CLIENT!!!"))

# Closing the socket
s.close()