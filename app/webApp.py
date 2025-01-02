from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
import plotly.io as pio
from datetime import datetime, timedelta
from DbConnexion import get_crypto, getAllcrypto_data, get_last_data, get_crypto_data
from Graph import listGraphPrice, listGraphVolume
from graphServer import *


app = Flask(__name__)


app.config['SECRET_KEY'] = 'your_secret_key'
# Configurer la base de données utilisateur
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Utilisateur.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Identifiant unique pour chaque utilisateur
    username = db.Column(db.String(150), unique=True, nullable=False)  # Nom d'utilisateur unique
    password = db.Column(db.String(150), nullable=False)  # Mot de passe sécurisé

    def __repr__(self):
        return f'<User {self.username}>'

# Créer la base de données
with app.app_context():
    db.create_all()  # Crée les tables dans la base de données

# Configuration de Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'Connexion'  # Redirige vers la page de connexion si l'utilisateur n'est pas connecté

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))





@app.route('/')
def index():
    return render_template('index.html')



# Route de connexion
@app.route('/Connexion', methods=['GET', 'POST'])
def Connexion():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Recherche l'utilisateur par son nom d'utilisateur
        user = User.query.filter_by(username=username).first()
        
        # Si l'utilisateur existe et le mot de passe est correct
        if user and check_password_hash(user.password, password):
            login_user(user)  # Connexion de l'utilisateur
            flash('Connexion réussie!', 'success')
            return redirect(url_for('index'))  # Redirige vers la page d'accueil après la connexion
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect.', 'danger')
    
    return render_template('Connexion.html')


@app.route('/Inscription', methods=['GET', 'POST'])
def Inscription():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Vérifie si l'utilisateur existe déjà
        if User.query.filter_by(username=username).first():
            flash("Cet utilisateur existe déjà.", "danger")
            return redirect(url_for('Inscription'))
        
        # Hachage du mot de passe avant de l'enregistrer
        hashed_password = generate_password_hash(password, method='sha256')
        
        # Ajoute l'utilisateur dans la base de données
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash("Utilisateur ajouté avec succès. Vous pouvez maintenant vous connecter.", "success")
        return redirect(url_for('Connexion'))  # Redirige vers la page de connexion après l'inscription
    return render_template('Inscription.html')  # Renvoie le formulaire d'inscription


@app.route('/ListeCrypto')
def ListeCrypto():
    table=get_last_data()
    return render_template('ListeCrypto.html', cryptoTable=table)


@app.route('/PricePage')
def PricePage():
    cryptoData_data=getAllcrypto_data()

    listGraph = listGraphPrice(cryptoData_data,10) 

    return render_template('PricePage.html', listGraph=listGraph)


@app.route('/VolumePage')
def VolumePage():
    cryptoData_data=getAllcrypto_data()

    listGraph = listGraphVolume(cryptoData_data,10) 

    return render_template('VolumePage.html', listGraph=listGraph)



    
@app.route('/GraphCrypto')
def GraphCrypto():
    id = request.args.get('id')
    
    # Récupérer la plage de temps sélectionnée par l'utilisateur
    time_range = request.args.get('time_range')
    
    # Calculer la date de début en fonction de la plage de temps
    if time_range == '1h':
        start_date = datetime.now() - timedelta(hours=1)
    elif time_range == '12h':
        start_date = datetime.now() - timedelta(hours=12)
    elif time_range == '1d':
        start_date = datetime.now() - timedelta(days=1)
    elif time_range == '7d':
        start_date = datetime.now() - timedelta(days=7)
    else:
        start_date = None  # Par défaut, on affiche les données récentes
    
    # Appeler la fonction pour récupérer les données filtrées
    crypto_data = get_crypto_data(id, start_date=start_date)
    
    # Créer les graphiques
    PriceGraph = createPriceGraph(crypto_data, id)
    VolumeGraph = createVolumeGraph(crypto_data, id)
    CandlestickGraph = createCandlestickGraph(crypto_data, id)
    HeatmapGraph = createHeatmap(crypto_data, id)
    
    # Convertir les graphiques en HTML
    PriceGraph_html = pio.to_html(PriceGraph, full_html=False)
    VolumeGraph_html = pio.to_html(VolumeGraph, full_html=False)
    CandlestickGraph_html = pio.to_html(CandlestickGraph, full_html=False)
    HeatmapGraph_html = pio.to_html(HeatmapGraph, full_html=False)
    
    return render_template('GraphCrypto.html', 
                           crypto=crypto_data,
                           PriceGraph=PriceGraph_html,
                           VolumeGraph=VolumeGraph_html,
                           CandlestickGraph=CandlestickGraph_html,
                           HeatmapGraph=HeatmapGraph_html)

if __name__ == '__main__':
    app.run(debug=True)
