import seq1
s1 = seq1.Seq()
s1.read_fasta("../Session04/U5.txt")

print(f"Sequence 1: (Length: {s1.len()}) {s1}")
print(f"\tBases: {s1.count()}")
print(f"\tRev: {s1.reverse()}")
print(f"\tComp: {s1.complement()}")