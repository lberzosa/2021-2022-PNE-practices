class Client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def ping(self):
        print("OK!")

    def __str__(self):
        sentence = "Connection to html at IP: " + str(self.ip) + " PORT: " + str(self.port)
        return sentence

    def talk(self, msg):
        import socket

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #crear el socket
        client_socket.connect((self.ip, self.port))

        msg_bytes = str.encode(msg) #mandar el mensaje
        client_socket.send(msg_bytes)

        response_bytes = client_socket.recv(2048) #recibir el mensaje
        response = response_bytes.decode("utf-8")
        client_socket.close()
        return response

    def debug_talk(self, msg):
        import socket
        import termcolor

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #crear el socket
        client_socket.connect((self.ip, self.port))

        print("to server: ", end="")
        termcolor.cprint(msg, "blue") #lo que envia el cliente está en azul
        msg_bytes = str.encode(msg) #mandar el mensaje
        client_socket.send(msg_bytes)

        response_bytes = client_socket.recv(2048) #recibir el mensaje
        response = response_bytes.decode("utf-8")
        print("from server:")
        print()
        termcolor.cprint(response, "green") #la respuesta del servidor está en verde
        client_socket.close()
        return response