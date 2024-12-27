from flask import Flask, render_template
import sqlite3
import plotly.graph_objects as go
from DbConnexion import get_crypto, get_crypto_data, get_last_data
from Graph import listGraphPrice, listGraphVolume

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
    cryptoData_data=get_crypto_data()

    listGraph = listGraphPrice(cryptoData_data,10) 

    return render_template('PricePage.html', listGraph=listGraph)


@app.route('/VolumePage')
def VolumePage():
    cryptoData_data=get_crypto_data()

    listGraph = listGraphVolume(cryptoData_data,10) 

    return render_template('VolumePage.html', listGraph=listGraph)


if __name__ == '__main__':
    app.run(debug=True)
