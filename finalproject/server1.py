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


def make_ensembl_request(endpoint,parameter):
    SERVER = 'rest.ensembl.org'
    PARAMS = '?content-type=application/json'

    print(f"\nServer: {SERVER}")
    conn = http.client.HTTPConnection(SERVER)

    try:
        conn.request("GET", endpoint + parameter + PARAMS)
    except ConnectionRefusedError:
        print("ERROR! Cannot connect to the Server")
        exit()

    r1 = conn.getresponse()
    print(f"Response received!: {r1.status} {r1.reason}\n")
    data1 = r1.read().decode("utf-8")
    answer = json.loads(data1)
    return answer


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


PORT = 8080


socketserver.TCPServer.allow_reuse_address = True


class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        termcolor.cprint(self.requestline, 'green')

        url_path = urlparse(self.path)
        path = url_path.path
        arguments = parse_qs(url_path.query)
        print("The old path was", self.path)
        print("The new path is", url_path.path)
        print("arguments", arguments)
        if self.path == "/":
            contents = read_html_file("index.html") \
                .render(context={"n_names": names_list})

        elif path == "/listSpecies":
            try:
                dict_answer = make_ensembl_request("/info/species", "")
                species = dict_answer["species"]
                limit = int(arguments["limit"][0])
                length = len(species)
                species_2 = []
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

            except KeyError:
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

        elif path == "/karyotype":
            try:
                speciess = arguments["speciess"][0].strip()
                dict_answer = make_ensembl_request("/info/assembly/", speciess)
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

        elif path == "/chromosomeLenght":
            try:
                species = str(arguments['specie'][0].strip())
                dict_answer = make_ensembl_request("/info/assembly/", species)
                chromo = int(arguments['chromosome'][0].strip())
                list = dict_answer["top_level_region"]
                line = []
                for i in range(0, len(list)):
                    line.append(list[i]["name"])
                site = line.index(str(chromo))
                line_2 = list[site]
                length = int(line_2["length"])
                if "json" in arguments:
                    contents = {"chromosome_lenght": length}
                else:
                    contents = read_html_file(path[1:] + ".html") \
                        .render(context={
                        "chromosome_lenght": length})
            except Exception:
                contents = read_html_file("error.html")\
                    .render()

        elif path == "/geneSeq":
            seq = arguments['seq'][0]
            key = genes_dict[seq]
            dict_answer = make_ensembl_request("/sequence/id/", str(key))
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
            dict_answer = make_ensembl_request("/sequence/id/", str(key))
            gene_info = dict_answer["desc"]
            seq_gene = dict_answer["seq"]
            s = seq1.Seq(seq_gene)
            info_split = gene_info.split(":")
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
            dict_answer = make_ensembl_request("/sequence/id/", key2)
            seq_1 = dict_answer["seq"]
            seq = seq1.Seq(seq_1)
            percentage_bases = seq.info()
            total_lenght = seq.len()
            if "json" in arguments:
                contents = {"percentages": percentage_bases, "t_lenght": total_lenght}
            else:
                contents = read_html_file(path[1:] + ".html")\
                    .render(context={
                    "percentages": percentage_bases,
                    "t_lenght": total_lenght
                })

        elif path == "/geneList":
            try:
                species = str(arguments['species'][0].strip())
                chromo = str(arguments['name'][0].strip())
                start = str(arguments['start'][0].strip())
                end = str(arguments['end'][0].strip())
                region = chromo + ":" + start + "-" + end
                answer = make_ensembl_request("/phenotype/region/", species + "/" + region)
                final_gene = []
                for i in range(0, len(answer)):
                    for c in answer[i]["phenotype_associations"]:
                        if "attributes" in c:
                            if "associated_gene" in c["attributes"]:
                                final_gene.append(c["attributes"]["associated_gene"])
                if "json" in arguments:
                    contents = {"gene": final_gene}
                else:
                    contents = read_html_file(path[1:] + ".html").render(context={"gene": final_gene})
            except KeyError:
                if "json" in arguments:
                    contents = {"ERROR": "A key error has occurred"}
                else:
                    contents = Path("error.html").read_text()
        else:
            contents = read_html_file("error.html") \
                .render()

        self.send_response(200)

        if "json" in arguments.keys():
            contents = json.dumps(contents)
            self.send_header('Content-Type', 'application/json')

        else:
            self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(contents.encode()))
        self.end_headers()
        self.wfile.write(str.encode(contents))

        return


Handler = TestHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:

    print("Serving at PORT", PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stoped by the user")
        httpd.server_close()

