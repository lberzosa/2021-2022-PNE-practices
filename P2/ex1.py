from client0 import Client

# -- Parameters of the html to talk to
IP = "192.168.1.45"
PORT = 8080

# -- Create a client object
c = Client(IP, PORT)

# -- Test the ping method
c.ping()

# -- Print the IP and PORTs
print(f"IP: {c.ip}, {c.port}")