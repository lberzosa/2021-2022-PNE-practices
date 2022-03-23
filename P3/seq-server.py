import socket
import termcolor
from seq import Seq

ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

PORT = 21000
IP = "localhost"

# -- Step 1: create the socket
ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# -- Optional: This is for avoiding the problem of Port already in use
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


def info(arg):
    print("Sequence: ", arg)
    print("Total lenght: ", len(arg))
    d = {"A": 0, "C": 0, "G": 0, "T": 0}
    for b in arg:
        d[b] += 1
    total = sum(d.values())
    for k, v in d.items():
        d[k] = [v, (v * 100) / total]
    final_dict = d
    message = ""
    for k, v in final_dict.items():
        message += k + ": " + str(v[0]) + " (" + str(round(v[1], 2)) + "%)" + "\n"
    return message


ls.bind((IP, PORT))
ls.listen()
print("The server is configured!")
while True:
    print("Waiting for Clients to connect")
    try:
        (cs, client_ip_port) = ls.accept()
    except KeyboardInterrupt:
        print("Server stopped by the user")
        ls.close()
        exit()
    else:
        print("A client has connected to the server!")
        msg_raw = cs.recv(2048)
        msg = msg_raw.decode()
        print(f"Message received: {msg}")

        split = msg.split(" ")
        cmd = split[0]

    # -- Manage message
    if cmd != "PING":
        arg = split[1]
    if cmd == "PING":
        response = "OK!"
        termcolor.cprint("PING COMMAND", "green")
        print("OK!")

    elif cmd == "GET":
        sequences = ["ADA.txt", "FRAT1.txt", "FXN.txt", "RNU6_269P.txt", "U5.txt"]
        FOLDER = "./sequences/"
        try:
            index = int(arg)
            filename = sequences[index]
            sequence = open(FOLDER + filename, "r").read()
            full_seq = sequence[sequence.find("\n"):].replace("\n", "")
            termcolor.cprint("GET", "green")
            print(full_seq)
            response = "GET " + str(index) + ":" + full_seq
            cs.send(response.encode())
        except ValueError:
            response = "The argument for the GET command must be from 0 to 4"

    elif cmd == "COMP":
        termcolor.cprint("COMP", "green")
        sequence = Seq(arg)
        print("Seq: ", sequence)
        response = "COMP " + str(sequence.complement())
        print("Comp: ", response)

    elif cmd == "INFO":
        termcolor.cprint("INFO", "green")
        response = info(arg)
        print(response)

    elif cmd == "REV":
        termcolor.cprint("REV", "green")
        reverse = arg[::-1]
        print(reverse)
        response = "REV " + str(reverse)

    elif cmd == "GENE":
        termcolor.cprint(cmd, "green")
        list_genes = ["U5.txt", "FRAT1.txt", "ADA.txt", "FXN.txt", "RNU6_269P.txt"]
        for l in list_genes:
            if arg == l:
                s = Seq()
                response = str(s.read_fasta(arg))
                print(response)

    else:
        response = "This command is not available in the server.\n"

    # -- The message has to be encoded into bytes
    cs.send(response.encode()) # cs es el client socket
    cs.close()


#except cs.error:
    #print("Problems using port {}. Do you have permission?".format(PORT))

#except KeyboardInterrupt:
    #print("Server stopped by the user")
    #cs.close()