import socket
import termcolor
from seq import Seq
import os

ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

PORT = 21000
IP = "localhost"

# -- Step 1: create the socket
ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# -- Optional: This is for avoiding the problem of Port already in use
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

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
        arg = Seq(arg)
        response = Seq.info(arg)
        print(response)

    elif cmd == "REV":
        termcolor.cprint("REV", "green")
        reverse = arg[::-1]
        print(reverse)
        response = "REV " + str(reverse)

    elif cmd == "GENE":
        seq1 = Seq()  # aqui lo mismo porque confunde la clase con la variable
        file = os.path.join(".", "sequences", f"{arg}")
        seq1.read_fasta(file)
        response = f"{seq1}\n"

    elif cmd == "ADD":
        termcolor.cprint("ADD", "green")
        arg = Seq(arg)
        response = Seq.sum(arg)
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