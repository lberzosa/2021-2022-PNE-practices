from client0 import Client
import P1.seq1
IP = "localhost"  #runnear con el html del session 08, porque necesitas a alguien que te escuche
PORT = 8080
FRAGMENTS = 5 #nos declaramos 2 constantes que no van a cambiar
BASES = 10

c = Client(IP, PORT)
print("sending a message to the server...")

filename = "../session04/FRAT1.txt"
seq = P1.seq1.Seq()
seq.read_fasta(filename)
c.debug_talk(f"sending FRAT1 to the server in fragments of 10 bases")
print(f"Gene FRAT1: {seq}")

start_index = 0
end_index = BASES
for f in range(1, FRAGMENTS + 1): #llega hasta el 5 [1, 6)
    fragment = seq.strbases[start_index:end_index]
    print(f"fragment {f}: {fragment}")
    c.debug_talk(fragment)
    start_index += BASES
    end_index += BASES #así no se me queda bloqueado en las primeras 10 bases