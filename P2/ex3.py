from client0 import Client
IP = "192.168.1.45"
PORT = 8080

c = Client(IP, PORT)
print("sending a message to the server...")
response = c.talk("Testing!!")
print(f"Response: {response}")