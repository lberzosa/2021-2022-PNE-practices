from P2.client0 import Client
PORT = 21000
IP = "localhost"

c = Client(IP, PORT)
c.talk("PING")
response = c.talk("PING")
print(response)
print(f"IP: {c.ip}, {c.port}")