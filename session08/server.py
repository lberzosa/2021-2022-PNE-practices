import socket

# Configure the Server's IP and PORT
PORT = 21000
IP = "212.128.253.64" #podemos usar IP = "localhost" (vincula las ips y no tengo que mirarlas)
MAX_OPEN_REQUESTS = 5

# Counting the number of connections
number_con = 0 #cuantos clientes se conectan

# create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #USAR SIEMPRE af_inet : el socket se comunica con el ip, stream: lo que se envia y recibe son bytes
try:
    serversocket.bind((IP, PORT)) #USAR SIEMPRE
    # become a server socket
    # MAX_OPEN_REQUESTS connect requests before refusing outside connections
    serversocket.listen(MAX_OPEN_REQUESTS) #USAR SIEMPRE

    while True:
        # accept connections from outside
        print("Waiting for connections at {}, {} ".format(IP, PORT))
        (clientsocket, address) = serversocket.accept() #aceptar la direccion y el socket del cliente

        # Another connection!e
        number_con += 1

        # Print the conection number
        print("CONNECTION: {}. From the IP: {}".format(number_con, address))

        # Read the message from the client, if any
        msg = clientsocket.recv(2048).decode("utf-8")
        print("Message from client: {}".format(msg))

        # Send the messag
        message = "Hello from the teacher's server" #message = len(msg)
        send_bytes = str.encode(message) # or str(message).encode()
        # We must write bytes, not a string
        clientsocket.send(send_bytes)
        clientsocket.close()

except socket.error:
    print("Problems using port {}. Do you have permission?".format(PORT))

except KeyboardInterrupt:
    print("Server stopped by the user")
    serversocket.close()