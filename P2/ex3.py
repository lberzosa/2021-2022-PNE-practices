from client0 import Client
IP = "localhost"
PORT = 8080

c = Client(IP, PORT)
print("sending a message to the server...")
response = c.talk("Testing!!")
print(f"Response: {response}")