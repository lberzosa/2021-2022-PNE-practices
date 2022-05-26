import http.client
import json
import termcolor

PORT = 8080
IP = "localhost"
SERVER = 'rest.ensembl.org'


def connect_server(endpoint,parameters):

    conn = http.client.HTTPConnection(IP, PORT)
    try:
        conn.request("GET", endpoint + parameters)
    except ConnectionRefusedError:
        print("ERROR! Cannot connect to the Server")
        exit()

    # -- Read the response message from the server
    r1 = conn.getresponse()

    # -- Print the status line
    print(f"Response received!: {r1.status} {r1.reason}\n")

    # -- Read the response's body
    data1 = r1.read().decode("utf-8")
    data2 = json.loads(data1)  # to transform it to a dictionary, it transforms the data into its corresponding type.
    return data2


species = connect_server("/listSpecies?", "limit=10&json=1")
print("list of species in a browser")
print(species)

karyotype = connect_server("/karyotype", "?speciess=horse&json=1")
print("karyotype of a species")
print(karyotype)

chromosome_length = connect_server("/chromosomeLength", "?specie=human&chromosome=9&json=1")
print("lenght of a chromosome")
print(chromosome_length)

gene_sequence = connect_server("/geneSeq", "?seq=FRAT1&json=1")
print("gene sequence")
print(gene_sequence)

gene_info = connect_server("/geneInfo", "?info=FRAT1&json=1")
print("gene info")
print(gene_info)

gene_calc = connect_server("/geneCalc", "?calc=FRAT1&json=1")
print("gene calculations")
print(gene_calc)

gene_list = connect_server("/geneList", "?species=homo_sapiens&name=9&start=20000&end=300000&json=1")
print("gene list")
print(gene_list)