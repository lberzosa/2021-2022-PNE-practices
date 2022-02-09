def count_bases(seq):
    d = {"A": 0, "C": 0, "G": 0, "T": 0}
    for b in seq:
        d[b] += 1
    return d

dna_seq = input("introduce the sequence: ")
print("total length:", len(dna_seq))
print(count_bases(dna_seq))
for k, v in count_bases(dna_seq).items():
    print(k + ":", v)