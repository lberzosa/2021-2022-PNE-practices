import seq0
filename = seq0.valid_filename()
seq = seq0.seq_read_fasta(filename)
print(seq[:20])