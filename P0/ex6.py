import seq0
filename = seq0.valid_filename()
seq = seq0.seq_read_fasta(filename)
new_seq = seq0.seq_reverse(seq)
print("fragment U5 gene -->", seq[:20])
print("reverse U5 gene -->", new_seq)