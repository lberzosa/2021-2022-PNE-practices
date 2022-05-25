import http.server
import socketserver
import termcolor
from pathlib import Path
import jinja2 as j
import http.client
from urllib.parse import parse_qs, urlparse
import json
import seq1

HTML_FOLDER = "./html/"
SERVER = 'rest.ensembl.org'
genes_dict = {"SRCAP": "ENSG00000080603",
              "FRAT1": "ENSG00000165879",
              "ADA": "ENSG00000196839",
              "FXN": "ENSG00000165060",
              "RNU6_269P": "ENSG00000212379",
              "MIR633": "ENSG00000207552",
              "TTTY4C": "ENSG00000228296",
              "RBMY2YP": "ENSG00000227633",
              "FGFR3": "ENSG00000068078",
              "KDR": "ENSG00000128052",
              "ANK2": "ENSG00000145362"}

names = genes_dict.keys()
names_list = []
for n in names:
    names_list.append(n)


def read_html_file(filename):
    contents = Path(HTML_FOLDER + filename).read_text()
    contents = j.Template(contents)
    return contents


def make_ensembl_request(url, params=""):
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
    #print(data2)
    return data2


def count_bases(seq):
    d = {"A": 0, "C": 0, "G": 0, "T": 0}
    for b in seq:
        d[b] += 1

    total = sum(d.values())
    for k,v in d.items():
        d[k] = [v, round((v * 100) / total,1)]
    return d


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
            contents = read_html_file("index.html") \
                .render(context={"n_names": names_list}) #poner aqui las que sean de desglosar una lista SIEMPRE

        elif path == "/listSpecies": #dos tipos de errores
            try:
                dict_answer = make_ensembl_request("/info/species", "")
                species = dict_answer["species"]  # queremos las especies en general
                limit = int(arguments["limit"][0])  # el 0 indica un valor para una llave. es lo que te va a pedir el servidor
                length = len(species)
                species_2 = [] #creamos una lista a la que vamos añadiendo las especies
                if limit > int(length):
                    message = "sorry, you picked a number too high"
                else:
                    message = ""
                    for i in range(0, limit):
                        species_2.append(species[i]['common_name'])
                if "json" in arguments:
                    contents = {"species": species_2, "number": length, "limit": limit}
                else:
                    contents = read_html_file(path[1:] + ".html")\
                        .render(context = {
                        "species": species_2,
                        "number": length,
                        "limit": limit,
                        "message": message
                    })

            except KeyError: #if there is no limit specified
                dict_answer = make_ensembl_request("/info/species", "")
                species = dict_answer["species"]
                length = len(species)
                species_3 = []
                for i in range(0, int(length)):
                    species_3.append(species[i]['common_name'])
                if "json" in arguments:
                    contents = {"all_species": species_3}
                else:
                    contents = read_html_file(path[1:] + ".html")\
                        .render(context={
                        "all_species": species_3
                    })
            except ValueError:
                if "json" in arguments:
                    contents = {"error": "sorry, you have a mistake"}
                else:
                    contents = read_html_file("error.html")\
                        .render()

        elif path == "/karyotype": #1 tipo de error
            try:
                speciess = arguments["speciess"][0].strip() #speciess lo ponemos aqui y en el html y es lo que aparecerá en el web, es porque queremos una en concreto
                dict_answer = make_ensembl_request("/info/assembly/" + speciess, "") #speciess es el diccionario concreto, una key una concreta
                karyotype = dict_answer["karyotype"]
                if "json" in arguments:
                    contents = {"karyotype": karyotype}
                else:
                    contents = read_html_file(path[1:] + ".html") \
                        .render(context={
                        "karyotype": karyotype})

            except KeyError:
                if "json" in arguments:
                    contents = {"error": "you got an incorrect species, try again"}
                else:
                    contents = read_html_file("error.html")\
                        .render()

        elif path == "/chromosomeLenght": #dos tipos de errores
            specie_3 = str(arguments['specie_3'][0].strip()) #quitamos espacios para que lo lea, solo lee el espacio sino
            dict_answer = make_ensembl_request("/info/assembly/" + specie_3, "")
            chromo = int(arguments['chromosome'][0].strip())
            try:
                list = dict_answer["top_level_region"]
                line = []
                for i in range(0, len(list)):
                    line.append(list[i]["name"]) #los agrupamos por especie (como en el 1)

                position = line.index(str(chromo))
                wanted_line = list[position]

                length = int(wanted_line["length"])

                if "json" in arguments:
                    contents = {"chromo": length}
                else:
                    contents = read_html_file(path[1:] + ".html") \
                        .render(context={
                        "chromo": length})

            except Exception:
                if "json" in arguments:
                    contents = {"error": "you got an error, please try again"}
                else:
                    contents = read_html_file("error.html")\
                        .render()

        elif path == "/geneSeq":
            seq = arguments['seq'][0]
            key = genes_dict[seq]
            dict_answer = make_ensembl_request("/sequence/id/" + str(key), "")
            info = dict_answer["seq"]
            if "json" in arguments:
                contents = {"sequence": info}
            else:
                contents = read_html_file(path[1:] + ".html") \
                    .render(context={
                    "sequence": info,
                })

        elif path == "/geneInfo":
            info = arguments["info"][0]
            key = genes_dict[info]
            dict_answer = make_ensembl_request("/sequence/id/" + str(key), "")
            gene_info = dict_answer["desc"] #usamos la descripcion para sacar la información del gen
            seq_gene = dict_answer["seq"]
            s = seq1.Seq(seq_gene)
            info_split = gene_info.split(":") #quitamos los dos puntos para así tener la distinta info y usarla
            start_gene = int(info_split[3])
            end_gene = int(info_split[4])
            chromosome = info_split[1]
            le = s.len()
            if "json" in arguments:
                contents = {"start": start_gene, "end": end_gene, "id": key, "le": le, "chromosome": chromosome}
            else:
                contents = read_html_file(path[1:] + ".html")\
                    .render(context={
                    "start": start_gene,
                    "end": end_gene,
                    "id": key,
                    "le": le,
                    "chromosome": chromosome,
                })

        elif path == "/geneCalc":
            gene_calc = arguments["calc"][0]
            key2 = genes_dict[gene_calc]
            dict_answer = make_ensembl_request("/sequence/id/" + key2, "")
            seq_1 = dict_answer["seq"] #necesitamos la secuencia para no tener una nullsequence
            seq = seq1.Seq(seq_1) #usamos la seq de la practica 1
            percentage_bases = seq.info() #aqui tenemos la funcion hecha hace mazo de los percentages
            total_lenght = seq.len()
            if "json" in arguments:
                contents = {"percentages": percentage_bases, "t_lenght": total_lenght}
            else:
                contents = read_html_file(path[1:] + ".html")\
                    .render(context={
                    "percentages": percentage_bases,
                    "t_lenght": total_lenght
                })

        elif path == "/geneList": #MIRAR ESTE QUE ESTA HECHO UN POCO LIO
            try:
                species = str(arguments["species"][0].strip())
                start = str(arguments["start"][0].strip())
                end = str(arguments["end"][0].strip())
                name = str(arguments["name"][0].strip())
                everything = name + ":" + start + "-" + end
                dict_answer = make_ensembl_request("phenotype/region/" + species + "/" + everything, ";feature_type=Variation")
                try:
                    if len(dict_answer) > 0:
                        gene_list = []
                        for i in range(0, len(dict_answer)):
                            for c in dict_answer[i]["phenotype_associations"]: #para las keys in la lista de phenotype
                                if "attributes" in c: #si existe esa key
                                    if "associated_gene" in c["attributes"]: #si existe ese value dentro de esa key
                                        gene_list.append(c["attributes"]["associated_gene"]) #appendear los values y las keys
                        if "json" in arguments:
                            contents = {"n_g": gene_list}
                        else:
                            contents = read_html_file(path[1:] + ".html") \
                                .render(context={
                                "n_g": gene_list
                            })

                    elif len(dict_answer) == 0:
                        contents = read_html_file("error.html") \
                            .render()
                except TypeError:
                    if "json" in arguments:
                        contents = {"error": "you got an error"}
                    else:
                        contents = read_html_file("error.html") \
                            .render()
            except KeyError:
                if "json" in arguments:
                    contents = {"error": "you got an error"}
                else:
                    contents = read_html_file("error.html") \
                        .render()

        # Generating the response message
        self.send_response(200)  # -- Status line: OK!

        if "json" in arguments.keys():
            contents = json.dumps(contents)
            self.send_header('Content-Type', 'application/json')

        else:
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

