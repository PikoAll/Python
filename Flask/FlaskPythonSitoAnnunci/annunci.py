from flask import Flask,render_template, request, session, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

'''
Il file bootstrap nella cartella static lo scaricato dal sito
'''


app = Flask(__name__)
app.config["SECRET_KEY"] = "a long and safe secret key"  #se usiamo i form questa e una cosa di sicurezza per evitare richieste fraudolente ed e obbigatoria per le sessioni
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://anonimo:123123123@localhost/annunci"  #per conettermi al db di postgresql passo user:password.../nomeDB
#app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://anonimo:123123123@localhost/"     #peppeGullo
app.config["SQLAlchemy_TRACK_MODIFICATIONS"] = False #consigliato da SQLAlchemy

db = SQLAlchemy(app) #istanzio


'''
Per evitare di creare il db su postgres manualmente, creauna classe come quella qua sotto, il nome della classe sara il nome della tabella, mentre gli attributi il nome delle colonne.
fatto cio apri un terminale python, se sei sul terminale linux scrivi python, entrato nel terminale python in questo caso fai (perche il file sichiama annunci) from annunci import db
poi fai db.create_all() ed esci dal terminale.
il tutto deve essere fatto con pgadmin chiuso.
facendo cio in automatico abbiamo creato la tabella dentro il db e lo possiamo vedere su pgadmin
'''
#creazione db per aministratore
class Amministratore(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(30))

# creazione db perinserimento annunci
class Annunci(db.Model):
    id = db.Column(db.Integer, primary_key = True)  #e autoincrement
    titolo = db.Column(db.String(50))
    descrizione = db.Column(db.String(300))

@app.route('/')
def homePage():

    # se l'utente e stato loggato cioe e in sessione allora..
    if 'user' in session:
        return redirect('/dashboard')

    risultati = Annunci.query.all()
    return render_template('index.html',risultati=risultati)


#creo dei riferimenti per verificare se  l'utente esiste qindi faccio qualcosa
#user = {'username':'jonny@j.it', 'password':'123'}
@app.route('/login', methods=['GET', 'POST'])
def login():
    #se il metodo e post allora salvo i dati dati
    if (request.method == 'POST'):
        username = request.form.get('username') #nel tag c'e name = username
        password = request.form.get('password') #nel tage c'e name = password

        #ora faccio una query per prendere il record relativo alla email
        amm = Amministratore.query.filter_by(email=username).first()
        print("zioooooooooooooooooooooo",amm)
        #if username == user['username'] and password == user['password']:
        if not(amm):
            return 'errore'
        elif username == amm.email and password == amm.password:
            session["user"] = username  #Salvo l'utente attualmente connesso nella sessione
            return redirect('/dashboard')  #utilizzare redirect()per reindirizzare a un URL passato


    return render_template('login.html')


@app.route('/logout')
def logout():
    # se l'utente e stato loggato cioe e in sessione allora..
    if 'user' in session:
        session.pop('user') # elimina dalla sessione l'utente
        return redirect('/')
    return render_template('logout.html')

@app.route('/dashboard')
def dashboard():
    # se l'utente e stato loggato cioe e in sessione allora..
    if 'user' in session:
        #prento tutti gli annunci che ci sono nel db per metterli visibili nella pagina
        risultati = Annunci.query.all()
        return render_template('dashboard.html',risultati=risultati)
    else:
        return redirect('/')

#profilo utente permette di aggiornare l'email o password
@app.route('/profilo',methods=['GET', 'POST'])
def profilo():
    if 'user' in session:

        if request.method == "POST":
            admin = Amministratore.query.filter_by(email = session['user']).first()

            #faccio un controllo se sulla pagina e stata inserito lemail o la Password
            if not request.form['email'] or not request.form['password']:
                return render_template('/profilo.html', user = session['user'])
            else:
                #cosi aggiorno i dati dal db
                admin.email = request.form['email']
                admin.password = request.form['password']
                db.session.commit()
                return render_template('/profilo.html', user = session['user'])

        return render_template('/profilo.html', user = session['user'])

    else:
        return redirect('/')


@app.route('/inserisci')
def inserisci():
    if 'user' in session:
        return render_template('inserisci.html')
    else:
        return redirect('/')

#relativa all'inserimento degli annunci
#questa route viene chiamata dall action derl tag form
@app.route('/process', methods=['POST'])
def process():
    titoloBreve = request.form['titoloBreve']  #alternativa al l'uso fatto nel metodo login per prendere il tag name
    descrizione = request.form['descrizione']
    #print('zioooooooooooooooooooooooooo',titoloBreve+'\n'+descrizione )

    #inserimento dell'anuncio nel db
    dati = Annunci(titolo=titoloBreve, descrizione=descrizione)  #i nomi delle colone sono = ai nomi delle variabili anche se anno nomi simili
    db.session.add(dati)  #ho aggiunto i dati
    db.session.commit()   #salvo la modifica
    #return titoloBreve+'\n'+descrizione
    return redirect('/dashboard')

@app.route('/elimina', methods=['GET'])
def elimina():
    if 'user' in session:
        idAnnuncio = request.values.get('id')  #dal link prendo la variabile id
        db.session.query(Annunci).filter(Annunci.id == idAnnuncio).delete()  #faccio una semplice queri con una wer se c'e quell id allora lo elimina
        db.session.commit()

        return redirect('/dashboard')
    else:
        return redirect('/index')

if __name__ == '__main__':
    app.run()
