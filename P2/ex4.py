from client0 import Client
import P1.seq1
IP = "localhost"  #runnear con el html del session 08, porque necesitas a alguien que te escuche
PORT = 8080

c = Client(IP, PORT)
print("sending a message to the server...")
list_genes = ["U5.txt", "ADA.txt", "FRAT1.txt"]
FOLDER = "../session04/"
for l in list_genes:
    filename = FOLDER + l
    seq = P1.seq1.Seq()
    seq.read_fasta(filename)
    c.debug_talk(f"sending {l} gene to the server...")
    c.debug_talk(str(seq)) #transformo seq a un string para que client me lo pueda leer (no esta dentro de un print) IMPORTANTE

