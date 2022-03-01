import seq1
s1 = seq1.Seq()
s2 = seq1.Seq("ACGTA")
s3 = seq1.Seq("invalid sequence")

print(f"Sequence 1: (Length: {s1.len()}) {s1}\n"
      f"Bases: {s1.count()}\n"
      f"Rev: {s1.reverse()}\n"
      f"Comp: {s1.complement()}")
print(f"Sequence 2: (Length: {s2.len()}) {s2}\n"
      f"Bases: {s2.count()}\n"
      f"Rev: {s2.reverse()}\n"
      f"Comp: {s2.complement()}")
print(f"Sequence 3: (Length: {s3.len()}) {s3}\n"
      f"Bases: {s3.count()}\n"
      f"Rev: {s3.reverse()}\n"
      f"Comp: {s3.complement()}")