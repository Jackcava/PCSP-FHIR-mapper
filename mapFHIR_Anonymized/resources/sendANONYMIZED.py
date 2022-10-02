import requests
import json
from requests.auth import HTTPBasicAuth, HTTPProxyAuth
import pandas as pd
from base64 import b64encode

def sendRes(dict_res,resource):
    address = "https://psp-demo-fhir.prep.sanit.cineca.it/fhir/" + resource #"https://fhir-server.dev.sanit.cineca.it/fhir-server/api/v4/Condition"
    proxies = {
        #"http": 
        #"https": 
    }
    
    #userAndPass = b64encode(b"usr:psw").decode("ascii")
    
    #Bauth = HTTPBasicAuth('usr', 'psw')

    Pauth = HTTPProxyAuth('usr','psw')

    headers = {'Accept': 'application/fhir+json','Authorization': 'Basic %s' % userAndPass,'Content-Type': 'application/fhir+json'}

    r = requests.post(address,headers=headers,data=dict_res,proxies=proxies,auth=Pauth,verify=False)

    print("\n********************************************************")
    print(r.status_code)
    print("********************************************************\n")
    print(r.text)

    d = json.loads(r.text)
    id_res = d["id"]

    return id_res
