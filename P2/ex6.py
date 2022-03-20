from client0 import Client
import P1.seq1
IP = "localhost"  #runnear con el html del session 08, porque necesitas a alguien que te escuche
PORT = 8080
PORT_2 = 8081

FRAGMENTS = 10
BASES = 10

c1 = Client(IP, PORT)
print(c1)
c2 = Client(IP, PORT_2) #usamos dos clientes
print(c2)
print("sending a message to the server...")

filename = "../session04/FRAT1.txt"
seq = P1.seq1.Seq()
seq.read_fasta(filename)
c1.debug_talk(f"sending FRAT1 to the server in fragments of 10 bases")
c2.debug_talk(f"sending FRAT1 to the server in fragments of 10 bases")

print(f"Gene FRAT1: {seq}")

start_index = 0
end_index = BASES
for f in range(1, FRAGMENTS + 1): #llega hasta el 5 [1, 6)
    fragment = seq.strbases[start_index:end_index]
    print(f"fragment {f}: {fragment}")
    if f % 2 == 0: #server 2
        c2.debug_talk(f"fragment {f}: {fragment}")
    else: #server 1
        c1.debug_talk(f"fragment {f}: {fragment}")
    start_index += BASES
    end_index += BASES #así no se me queda bloqueado en las primeras 10 bases