import seq1
list_genes = ["U5.txt", "FRAT1.txt", "ADA.txt", "FXN.txt", "RNU6_269P.txt"]
FOLDER = "../session04/"
for f in list_genes:
    filename = FOLDER + f
    s1 = seq1.Seq()
    s1.read_fasta(filename)
    u2 = s1.most_base()
    print("gen", f,":", "most frequent base -->", u2[1]) #[1] significa que me imprima el carácter 1 que es bases (count seria el 0)