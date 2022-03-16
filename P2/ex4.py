from client0 import Client
IP = "localhost"  #runnear con el html del session 08, porque necesitas a alguien que te escuche
PORT = 8080

c = Client(IP, PORT)
print("sending a message to the html...")
response = c.talk("Testing!!")
print(f"Response: {response}")