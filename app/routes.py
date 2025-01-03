from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
import plotly.io as pio
from datetime import datetime, timedelta
from .DbConnexion import *
from .graphServer import *
from .models import User, db, Crypto, Alerte  

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/Connexion', methods=['GET', 'POST'])
def Connexion():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Connexion réussie!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect.')
    return render_template('Connexion.html')

@main.route('/Inscription', methods=['GET', 'POST'])
def Inscription():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash("Cet utilisateur existe déjà.")
            return redirect(url_for('main.Inscription'))
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('main.Connexion'))
    return render_template('Inscription.html')

@main.route('/profil')
@login_required
def profil():
    alertes = Alerte.query.filter_by(user_id=current_user.id).all()
    
    return render_template('profil.html', username=current_user.username, email=current_user.email, alertes=alertes)

@main.route('/logout')
@login_required  # S'assure que l'utilisateur est connecté avant de pouvoir se déconnecter
def logout():
    logout_user()  # Déconnecte l'utilisateur
    return redirect(url_for('main.index'))  # Redirige l'utilisateur vers la page d'accueil ou une autre page


@main.route('/Alertes', methods=['GET', 'POST'])
@login_required
def Alertes():
    db.create_all()
    populate_crypto_table()######
    if request.method == 'POST':
        crypto_id = request.form['crypto_id']
        condition = request.form['condition']  # 'price', 'percentage', etc.
        threshold_value = float(request.form['threshold_value'])
        type_alert = request.form['type_alert']  # 'greater_than', 'less_than', etc.
        
        # Créer une nouvelle alerte pour l'utilisateur
        new_alert = Alerte(user_id=current_user.id, 
                           crypto_id=crypto_id, 
                           condition=condition, 
                           threshold_value=threshold_value,
                           type_alert=type_alert)
        
        db.session.add(new_alert)
        db.session.commit()
        
        flash('Alerte créée avec succès!', 'success')
        return redirect(url_for('main.index'))

    tableCrypto = get_last_data() # Récupérer la liste des cryptomonnaies
    cryptos = []
    for row in tableCrypto :
        cryptos.append(row['crypto_id'])
    return render_template('Alertes.html', cryptos=cryptos)

@main.route('/delete_alert/<int:alerte_id>', methods=['POST'])
@login_required
def delete_alert(alerte_id):
    # Vérifier si l'alerte appartient à l'utilisateur connecté
    alerte = Alerte.query.filter_by(id=alerte_id, user_id=current_user.id).first()
    
    if alerte:
        # Supprimer l'alerte
        db.session.delete(alerte)
        db.session.commit()
    return redirect(url_for('main.profil'))  # Rediriger l'utilisateur vers la page du profil








@main.route('/ListeCrypto')
def ListeCrypto():
    table = get_last_data()
    return render_template('ListeCrypto.html', cryptoTable=table)

@main.route('/GraphCrypto')
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
    PredictGraph = createPredictGraph(crypto_data, id)
    VolumeGraph = createVolumeGraph(crypto_data, id)
    CandlestickGraph = createCandlestickGraph(crypto_data, id)
    HeatmapGraph = createHeatmap(crypto_data, id)

    
    # Convertir les graphiques en HTML
    PriceGraph_html = pio.to_html(PriceGraph, full_html=False)
    VolumeGraph_html = pio.to_html(VolumeGraph, full_html=False)
    CandlestickGraph_html = pio.to_html(CandlestickGraph, full_html=False)
    HeatmapGraph_html = pio.to_html(HeatmapGraph, full_html=False)
    prediction_graph_html = pio.to_html(PredictGraph, full_html=False)
    
    return render_template('GraphCrypto.html', 
                           crypto=crypto_data,
                           PriceGraph=PriceGraph_html,
                           VolumeGraph=VolumeGraph_html,
                           CandlestickGraph=CandlestickGraph_html,
                           HeatmapGraph=HeatmapGraph_html,
                           PredictGraph=prediction_graph_html)
