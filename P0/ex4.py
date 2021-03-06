import seq0
list_genes = ["U5.txt", "FRAT1.txt", "ADA.txt", "FXN.txt", "RNU6_269P.txt"]
FOLDER = "../Session04/"

for f in list_genes:
    filename = FOLDER + f
    seq = seq0.seq_read_fasta(filename)
    count_A, count_C, count_G, count_T = seq0.count_bases_seq(seq)
    print("GEN", f)
    print("A:", count_A, "\nC:", count_C, "\nG:", count_G, "\nT:", count_T)