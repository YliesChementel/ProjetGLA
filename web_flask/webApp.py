from flask import Flask, render_template, flash, request
import sqlite3
import plotly.io as pio
from DbConnexion import get_crypto, getAllcrypto_data, get_last_data, get_crypto_data
from Graph import listGraphPrice, listGraphVolume
from graphServer import *


app = Flask(__name__)

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
    crypto = get_crypto_data(id)
    
    # Créer les graphiques
    PriceGraph = createPriceGraph(crypto, id)
    VolumeGraph = createVolumeGraph(crypto, id)
    CandlestickGraph = createCandlestickGraph(crypto, id)
    HeatmapGraph = createHeatmap(crypto, id)
    
    # Convertir les graphiques en HTML
    PriceGraph_html = pio.to_html(PriceGraph, full_html=False)
    VolumeGraph_html = pio.to_html(VolumeGraph, full_html=False)
    CandlestickGraph_html = pio.to_html(CandlestickGraph, full_html=False)
    HeatmapGraph_html = pio.to_html(HeatmapGraph, full_html=False)
    
    return render_template('GraphCrypto.html', 
                           crypto=crypto,
                           PriceGraph=PriceGraph_html,
                           VolumeGraph=VolumeGraph_html,
                           CandlestickGraph=CandlestickGraph_html,
                           HeatmapGraph=HeatmapGraph_html)

if __name__ == '__main__':
    app.run(debug=True)
