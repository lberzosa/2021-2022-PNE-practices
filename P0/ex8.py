import seq0
list_genes = ["U5.txt", "FRAT1.txt", "ADA.txt", "FXN.txt", "RNU6_269P.txt"]
FOLDER = "../Session04/"
for f in list_genes:
    filename = FOLDER + f
    seq = seq0.seq_read_fasta(filename)
    most_base = seq0.most_base(seq)
    print("gen", f,":", "most frequent base -->", most_base)