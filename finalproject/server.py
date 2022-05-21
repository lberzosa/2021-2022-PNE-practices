import http.server
import socketserver
import jinja2 as j
from urllib.parse import parse_qs, urlparse

SERVER = 'rest.ensembl.org'
ENDPOINT = "/"
PARAMS = "?content-type=application/json"

URL = ENDPOINT + PARAMS

#we want to use the dictionary of P7
#do a while for something