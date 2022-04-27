# -- Example of a client that uses the HTTP.client library
# -- for requesting the main page from the server
import http.client
import json

SERVER = 'rest.ensembl.org' #this is the same #modificar algo para el 3
ENDPOINT = "/sequence/id"
PARAMS = "?content-type=application/json" #this is the same

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

for k, v in genes_dict.items():  # abrir diccionarios
    print(k, "--->", v)

print(f"\nConnecting to server: {SERVER}\n")

# Connect with the server
conn = http.client.HTTPConnection(SERVER)

# -- Send the request message, using the GET method. We are
# -- requesting the main page (/)
try:
    conn.request("GET", ENDPOINT + PARAMS) #only use the endpoint + params (NEVER THE SERVER QUESTION IN EXAM)
    # -- Read the response message from the server
    r1 = conn.getresponse()

    # -- Print the status line
    print(f"Response received!: {r1.status} {r1.reason}\n")

    # -- Read the response's body
    data1 = r1.read().decode("utf-8")
    data1 = json.loads(data1) #the json thing is getting the integer/float/str and transforming the data in the appropiate language to make a dictionary
    print(f"CONTENT: {genes_dict}")

except ConnectionRefusedError:
    print("ERROR! Cannot connect to the Server")
    exit()