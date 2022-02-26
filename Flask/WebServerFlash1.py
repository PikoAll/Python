# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

'''
non so se va fatto ogni volta da terminale
export FLASK_APP=nome_file.py
'''

from flask import Flask, request, Response

app = Flask(__name__)

@app.get("/")
def ritorna():  
    return "hello word"


#@app.post("/inserisci")
@app.route('/inserisci', methods=['POST'])
def inserisci():
   print('hola')
   ricevuto="provaMesssaggio Mho"
 
   print(request.data)
   return Response('okk')
   ''' print("sono dentro il metodo inserisci")
    if request.is_json:
        print('')
        #print('holaa',request.get_json())
        #print('\n\n', request.get_json['name'])
        return 'ok'
    print('non e json')'''

app.run(ssl_context='adhoc',port=8080)  #il parametro devtro serve per creare conessione https, senza abbiamo http  #posso passare la porta come parametro #strano ma funziona con ...
#app.run()