import seq0
filename = seq0.valid_filename()
seq = seq0.seq_read_fasta(filename)
print("fragment U5 gene -->", seq[:20])
print("complement U5 gene -->", seq0.seq_complement(seq))
