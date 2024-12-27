from flask import Flask, render_template
import sqlite3
import plotly.graph_objects as go
from DbConnexion import get_crypto, get_crypto_data,get_last_data

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/acceuil')
def acceuil():
    return render_template('acceuil.html')  # Accès à la page d'accueil spécifique


@app.route('/ListeCrypto')
def ListeCrypto():
    table=get_last_data()
    return render_template('ListeCrypto.html', cryptoTable=table)



@app.route('/PricePage')
def PricePage():
    cryptoData_data=get_crypto_data()

    # Génération des graphiques des prix
    prices, volumes = graphPricesAndVolumes(cryptoData_data)

    graphPriceBTC = prices[0].to_html(full_html=False)
    graphPriceETH = prices[1].to_html(full_html=False)
    graphPriceUDST = prices[2].to_html(full_html=False)
    graphPriceSOL = prices[3].to_html(full_html=False)
    graphPriceBNB = prices[4].to_html(full_html=False)

    return render_template('PricePage.html',
        graphPriceBTC=graphPriceBTC,
        graphPriceETH=graphPriceETH,
        graphPriceUDST=graphPriceUDST,
        graphPriceSOL=graphPriceSOL,
        graphPriceBNB=graphPriceBNB
    )

@app.route('/VolumePage')
def VolumePage():  # Renommé pour éviter le conflit de nom
    cryptoData_data=get_crypto_data()

    # Génération des graphiques des volumes
    prices, volumes = graphPricesAndVolumes(cryptoData_data)

    graphVolumeBTC = volumes[0].to_html(full_html=False)
    graphVolumeETH = volumes[1].to_html(full_html=False)
    graphVolumeUDST = volumes[2].to_html(full_html=False)
    graphVolumeSOL = volumes[3].to_html(full_html=False)
    graphVolumeBNB = volumes[4].to_html(full_html=False)

    return render_template('VolumePage.html',
        graphVolumeBTC=graphVolumeBTC,
        graphVolumeETH=graphVolumeETH,
        graphVolumeUDST=graphVolumeUDST,
        graphVolumeSOL=graphVolumeSOL,
        graphVolumeBNB=graphVolumeBNB
    )

def graphPricesAndVolumes(cryptoData_data):
    dates = []
    pricesBTC, pricesETH, pricesUSDT, pricesSOL, pricesBNB = [], [], [], [], []
    volumesBTC, volumesETH, volumesUSDT, volumesSOL, volumesBNB = [], [], [], [], []

    for data in cryptoData_data:
        if data['crypto_id'] == "bitcoin":
            pricesBTC.append(data['price'])
            volumesBTC.append(data['volume'])
            dates.append(data['fetchTime'])
        if data['crypto_id'] == "ethereum":
            pricesETH.append(data['price'])
            volumesETH.append(data['volume'])
        if data['crypto_id'] == "tether":
            pricesUSDT.append(data['price'])
            volumesUSDT.append(data['volume'])
        if data['crypto_id'] == "solana":
            pricesSOL.append(data['price'])
            volumesSOL.append(data['volume'])
        if data['crypto_id'] == "binance-coin":
            pricesBNB.append(data['price'])
            volumesBNB.append(data['volume'])

    # Création des graphiques pour les prix
    figBTC = go.Figure()
    figETH = go.Figure()
    figUDST = go.Figure()
    figSOL = go.Figure()
    figBNB = go.Figure()

    figBTC.add_trace(go.Scatter(x=dates, y=pricesBTC, name='Prix Bitcoin'))
    figETH.add_trace(go.Scatter(x=dates, y=pricesETH,  name='Prix Ethereum'))
    figUDST.add_trace(go.Scatter(x=dates, y=pricesUSDT, name='Prix Tether'))
    figSOL.add_trace(go.Scatter(x=dates, y=pricesSOL, name='Prix Solana'))
    figBNB.add_trace(go.Scatter(x=dates, y=pricesBNB, name='Prix BNB'))

    common_layout = {
        'xaxis': {'title': 'Date'},
        'yaxis': {'title': 'Prix (USD)'},
        'hovermode': 'closest',  # Affichage des valeurs au survol
        'showlegend': True,  # Montrer la légende
        'plot_bgcolor': 'rgba(255, 255, 255, 0)',  # Fond transparent
        'paper_bgcolor': 'rgba(255, 255, 255, 0)',  # Fond du graphique transparent
        'font': {'family': 'Arial', 'size': 12, 'color': 'black'},
        'modebar': {'remove': ['zoom', 'pan', 'resetScale', 'zoomIn', 'zoomOut', 'sendDataToCloud']},  # Désactive certaines options du modebar
    }

    
    figBTC.update_layout(title='Évolution du Prix du BTC', **common_layout)
    figETH.update_layout(title='Évolution du Prix de l\'ETH', **common_layout)
    figUDST.update_layout(title='Évolution du Prix du UDST', **common_layout)
    figSOL.update_layout(title='Évolution du Prix du SOL', **common_layout)
    figBNB.update_layout(title='Évolution du Prix du BNB', **common_layout)
    

    # Création des graphiques pour les volumes
    volBTC = go.Figure()
    volETH = go.Figure()
    volUDST = go.Figure()
    volSOL = go.Figure()
    volBNB = go.Figure()

    volBTC.add_trace(go.Scatter(x=dates, y=volumesBTC, name='Volume Bitcoin'))
    volETH.add_trace(go.Scatter(x=dates, y=volumesETH, name='Volume Ethereum'))
    volUDST.add_trace(go.Scatter(x=dates, y=volumesUSDT, name='Volume Tether'))
    volSOL.add_trace(go.Scatter(x=dates, y=volumesSOL, name='Volume Solana'))
    volBNB.add_trace(go.Scatter(x=dates, y=volumesBNB, name='Volume BNB'))

    volBTC.update_layout(title='Évolution du Volume du BTC', xaxis_title='Date', yaxis_title='Volume')
    volETH.update_layout(title='Évolution du Volume du ETH', xaxis_title='Date', yaxis_title='Volume')
    volUDST.update_layout(title='Évolution du Volume du UDST', xaxis_title='Date', yaxis_title='Volume')
    volSOL.update_layout(title='Évolution du Volume du SOL', xaxis_title='Date', yaxis_title='Volume')
    volBNB.update_layout(title='Évolution du Volume du BNB', xaxis_title='Date', yaxis_title='Volume')

    return (figBTC, figETH, figUDST, figSOL, figBNB), (volBTC, volETH, volUDST, volSOL, volBNB)

if __name__ == '__main__':
    app.run(debug=True)
