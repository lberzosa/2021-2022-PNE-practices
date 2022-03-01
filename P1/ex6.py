import seq1
s1 = seq1.Seq()
s2 = seq1.Seq("ACGTA")
s3 = seq1.Seq("invalid sequence")

print(f"Sequence 1: (Length: {s1.len()}) {s1}")
print(s1.count())
print(f"Sequence 2: (Length: {s2.len()}) {s2}")
print(s2.count())
print(f"Sequence 3: (Length: {s3.len()}) {s3}")
print(s3.count())