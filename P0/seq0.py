def seq_ping():
    print("ok")

def valid_filename():
    exit = False
    while not exit:
        filename = input("what file do you want to open: ")
        try:
            f = open(filename, "r")
            exit = True
            return filename
        except FileNotFoundError:
            print("file does not exist")

def seq_read_fasta(filename):
    seq = open(filename, "r").read()
    seq = seq[seq.find("\n"):].replace("\n", "")
    return seq

def count_bases_seq(seq):
    count_A = 0
    count_C = 0
    count_G = 0
    count_T = 0
    for i in seq:
        if i == "A":
            count_A += 1
        elif i == "C":
            count_C += 1
        elif i == "G":
            count_G += 1
        elif i == "T":
            count_T += 1
    return count_A, count_C, count_G, count_T

def count_bases(seq):
    d = {"A": 0, "C": 0, "G": 0, "T": 0}
    for b in seq:
        d[b] += 1
    return d

def seq_reverse(seq):
    new_seq = seq[:20]
    new_seq = new_seq[::-1] #[::-1] empieza por el final del string y va hasta la posicion -1 sin incluirlo
    return new_seq

def seq_complement(seq):
    new_seq = seq[:20]
    complement = {"A": "T", "C": "G", "G": "C", "T": "A"}
    return "".join([complement[base] for base in new_seq]) #sustituimos una base por otra (el value por el key)
