import socket
import termcolor
import P1.seq1

ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

PORT = 21000
IP = "localhost"
list_genes = ["U5.txt", "FRAT1.txt", "ADA.txt", "FXN.txt", "RNU6_269P.txt"]

# -- Step 1: create the socket
ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# -- Optional: This is for avoiding the problem of Port already in use
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    ls.bind((IP, PORT))
    ls.listen()
    print("The server is configured!")
    while True:
        print("Waiting for Clients to connect")
        (cs, client_ip_port) = ls.accept()
        print("A client has connected to the server!")

        # -- Read the message from the client
        # -- The received message is in raw bytes
        msg_raw = cs.recv(2048)
        msg = msg_raw.decode().replace("\n", "").strip()
        cmd = msg.split(' ')[0]

        # -- Print the received message
        if cmd != "PING":
            arg = msg.split(' ')[1]
            print(f"Message received: {msg}")

            # -- Manage message
        if cmd == "PING":
            response = "OK!\n"
            termcolor.cprint("PING command!", "green")
            print(response)

        elif cmd == "GET":
            sequence_number = int(arg[1])
            gene = list_genes[sequence_number]
            seq = P1.seq1.Seq()
            seq.read_fasta()

        else:
            response = "This command is not available in the server.\n"


        # -- The message has to be encoded into bytes
        cs.send(response.encode())

        # -- Close the data socket
        cs.close()
except cs.error:
    print("Problems using port {}. Do you have permission?".format(PORT))

except KeyboardInterrupt:
    print("Server stopped by the user")
    cs.close()