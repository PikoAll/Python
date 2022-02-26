#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 18:43:04 2022

@author: anonimo
"""

import requests

prova=requests.get("host##:port##/",verify=False)  #il secondo parametro e uguale a false per evitare  che dice che la pagina non e sicura..
#prova=requests.get("http://127.0.0.1:5000/")  #il secondo parametro e uguale a false per evitare  che dice che la pagina non e sicura..

print(prova)
print(prova.text)
print('\n\ninvio \n\n')
#requests.post("https://127.0.0.1:5000/inserisci -X POST -H 'Content-Type: application/json' -d '{'name':'Germany', 'capital': 'Berlin', 'area': 357022}'",verify=False) 
r=requests.post("host##:port##/inserisci",data='ciaooooo22',verify=False,allow_redirects=True) 
print('\n\ninviato \n\n')
#r=requests.post("http://127.0.0.1:5000/inserisci",data='ciaooooo') 

print(r)

