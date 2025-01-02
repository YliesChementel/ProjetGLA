from flask import Flask, render_template, flash, request
import sqlite3
import plotly.io as pio
from datetime import datetime, timedelta
from DbConnexion import get_crypto, getAllcrypto_data, get_last_data, get_crypto_data
from Graph import listGraphPrice, listGraphVolume
from graphServer import *


app = Flask(__name__)

# Configurer la base de données utilisateur
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Utilisateur.db'

@app.route('/')
def index():
    return render_template('index.html')

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


@app.route('/Connexion')
def Connexion():
    return render_template('Connexion.html')

@app.route('/Inscription')
def Inscription():
    return render_template('Inscription.html')
    
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
