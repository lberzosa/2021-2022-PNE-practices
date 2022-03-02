class Client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def ping(self):
        print("OK!")

    def __str__(self):
        sentence = "Connection to server at IP: " + str(self.ip) + " PORT: " + str(self.port)
        return sentence