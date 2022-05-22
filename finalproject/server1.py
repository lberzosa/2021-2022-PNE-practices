import http.server
import socketserver
import termcolor
from pathlib import Path
import jinja2 as j
import http.client
from urllib.parse import parse_qs, urlparse
import json

HTML_FOLDER = "./html/"
SERVER = 'rest.ensembl.org'
PARAMS = '?content-type=application/json'

def read_html_file(filename):
    contents = Path(HTML_FOLDER + filename).read_text()
    contents = j.Template(contents)
    return contents


def make_ensembl_request(url, params):
    conn = http.client.HTTPConnection(SERVER)
    parameters = '?content-type=application/json'
    try:
       conn.request("GET", url + parameters + params)

    except ConnectionRefusedError:
        print("ERROR! Cannot connect to the Server")
        exit()

    r1 = conn.getresponse()

    print(f"Response received!: {r1.status} {r1.reason} \n")
    data1 = r1.read().decode('utf-8')  #this is the dictionary

    data2 = json.loads(data1)
    return data2

def count_bases(seq):
    d = {"A": 0, "C": 0, "G": 0, "T": 0}
    for b in seq:
        d[b] += 1

    total = sum(d.values())
    for k,v in d.items():
        d[k] = [v, round((v * 100) / total,1)]
    return d

def complement(seq):
    compl = ""
    for g in seq:
        if g == "A":
            compl += "T"
        elif g == "T":
            compl += "A"
        elif g == "C":
            compl += "G"
        elif g == "G":
            compl += "C"

    return compl

def convert_message(base_count):
    message = ""
    for k,v in base_count.items():
        message += k + ": " + str(v[0]) + " (" + str(v[1]) + "%)" + "\n"
    return message

def info_operation(arg):
    base_count = count_bases(arg)
    response = "<p> Sequence: " + arg + "</p>"
    response += "<p> Total length: " + str(len(arg)) + "</p>"
    response += convert_message(base_count)
    return response

# Define the Server's port
PORT = 8081

# -- This is for preventing the error: "Port already in use"
socketserver.TCPServer.allow_reuse_address = True


# Class with our Handler. It is a called derived from BaseHTTPRequestHandler
# It means that our class inheritates all his methods and properties
class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        """This method is called whenever the client invokes the GET method
        in the HTTP protocol request"""
        # Print the request line
        termcolor.cprint(self.requestline, 'green')

        url_path = urlparse(self.path)
        path = url_path.path #this is the url
        arguments = parse_qs(url_path.query)  #esto es lo que conviertes en diccionario
        print("The old path was", self.path)
        print("The new path is", url_path.path)
        print("arguments", arguments)
        # Message to send back to the client
        if self.path == "/": # son los endpoints
            contents = read_html_file("index.html")\
                .render() # render es para pasar el jinja a texto (formato json)

        elif path == "/listSpecies":
            dict_answer = make_ensembl_request("/info/species", "")
            limit = int(arguments["limit"][0])  # el 0 indica un valor para una llave. es lo que te va a pedir el servidor
            species = dict_answer["species"]
            length = len(species)
            species_2 = []
            for i in range(0, limit):
                species_2.append(species[i]['common_name'])
            contents = read_html_file(path[1:] + ".html")\
                .render(context = {
                "species": species_2,
                "number": length,
                "limit": limit
            })
        elif path == "/karyotype":
            species2 = arguments["species2"][0]
            dict_answer = make_ensembl_request("/info/species" + species2, "")
            karyotype = dict_answer['karyotype']
            contents = read_html_file(path[1:] + ".html") \
                .render(context={
                "chromosomes": karyotype
            })
        elif path == "/operation":
            sequence = arguments["msg"][0]
            operation = arguments["option"][0]
            print(operation)

            if operation == "Rev":
                contents = read_html_file(path[1:] + ".html") \
                    .render(context={
                    "sequence": sequence,
                    "operation": operation,
                    "result": sequence[::-1]
                })
            elif operation == "Info":
                contents = read_html_file(path[1:] + ".html") \
                    .render(context={
                    "sequence": sequence,
                    "operation": operation,
                    "result": info_operation(sequence)
                })

            elif operation == "Comp":
                print(operation, "test")
                contents = read_html_file(path[1:] + ".html") \
                    .render(context={
                    "sequence": sequence,
                    "operation": operation,
                    "result": complement(sequence)
                    })
        else:
            contents = "I am the happy server! :-)"


        # Generating the response message
        self.send_response(200)  # -- Status line: OK!

        # Define the content-type header:
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(contents.encode()))

        # The header is finished
        self.end_headers()

        # Send the response message
        self.wfile.write(contents.encode())

        return


# ------------------------
# - Server MAIN program
# ------------------------
# -- Set the new handler
Handler = TestHandler

# -- Open the socket server
with socketserver.TCPServer(("", PORT), Handler) as httpd:

    print("Serving at PORT", PORT)

    # -- Main loop: Attend the client. Whenever there is a new
    # -- clint, the handler is called
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stoped by the user")
        httpd.server_close()