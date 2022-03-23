import socket
from client import Client
IP = "localhost"
PORT = 21000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))
c = Client(IP, PORT)

#1:
print("PING...")
s.send(str.encode("PING"))
msg = s.recv(2048)
print(msg.decode("utf-8"))

#2:
print("GET...")
list = ["0", "1", "2", "3"]
for n in list:
    msg = c.debug_talk("GET " + n)
    print(msg)

seq = c.debug_talk("GET 0")
seq = seq.split("GET 0:")[1]


#4:
print("COMP...")
msg = c.debug_talk("COMP " + seq)
print(msg)

#5:
print("REV...")
msg = c.debug_talk("REV " + seq)
print(msg)

#6:
print("GENE...")
list_genes = ["U5.txt", "FRAT1.txt", "ADA.txt", "FXN.txt", "RNU6_269P.txt"]
for g in list_genes:
    print("TESTING", g, "...")
    response = c.talk("GENE g")
    print(response)

#3:
print("INFO...")
msg = c.debug_talk("INFO " + seq)
print(msg)

s.close()
