from seq1 import Seq

st1 = "ACCTGC"
st2 = "Hello? Am I a valid sequence?"
sequence_list = []
str_list = ["AGGTGC", "Hello? Am I a valid sequence?"]

for st in str_list:
    if Seq.valid_sequence2(st):
        sequence_list.append(Seq(st))
    else:
        sequence_list.append(Seq("ERROR"))

for i in range(0, len(sequence_list)):
    print("Sequence", str(i) + ":", sequence_list[i])

