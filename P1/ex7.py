import seq1
s1 = seq1.Seq()
s2 = seq1.Seq("ACGTA")
s3 = seq1.Seq("invalid sequence")

print(f"Sequence 1: (Length: {s1.len()}) {s1}")
print(f"\tBases: {s1.count()}")
print(f"\tRev: {s1.reverse()}")
print(f"Sequence 2: (Length: {s2.len()}) {s2}")
print(f"\tBases: {s2.count()}")
print(f"\tRev: {s2.reverse()}")
print(f"Sequence 3: (Length: {s3.len()}) {s3}")
print(f"\tBases: {s3.count()}")
print(f"\tRev: {s3.reverse()}")