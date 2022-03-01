import seq1
s1 = seq1.Seq()
s2 = seq1.Seq("ACGTA")
s3 = seq1.Seq("invalid sequence")

print(f"Sequence 1: (Length: {s1.len()}) {s1}")
print(f"A: {s1.count_base()[0]}, C: {s1.count_base()[1]}, G: {s1.count_base()[2]}, T: {s1.count_base()[3]}")
print(f"Sequence 2: (Length: {s2.len()}) {s2}")
print(f"A: {s2.count_base()[0]}, C: {s2.count_base()[1]}, G: {s2.count_base()[2]}, T: {s2.count_base()[3]}")
print(f"Sequence 3: (Length: {s3.len()}) {s3}")
print(f"A: {s3.count_base()[0]}, C: {s3.count_base()[1]}, G: {s3.count_base()[2]}, T: {s3.count_base()[3]}")