import seq0
list_genes = ["U5.txt", "FRAT1.txt", "ADA.txt", "FXN.txt", "RNU6_269P.txt"]
for l in list_genes:
    print(l, "-->", len(seq0.seq_read_fasta("../session04/" + l)))