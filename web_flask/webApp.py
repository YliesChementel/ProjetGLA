from flask import Flask, render_template
import sqlite3
import plotly.graph_objects as go

app = Flask(__name__)

@app.route('/')
def index():
    # Connexion à la base de données Crypto.db
    connCrypto = sqlite3.connect('Crypto.db')
    connCrypto.row_factory = sqlite3.Row

    # Récupération des données de la base
    crypto_data = connCrypto.execute('SELECT * FROM Crypto').fetchall()
    cryptoData_data = connCrypto.execute('SELECT * FROM CryptoData').fetchall()

    connCrypto.close()

    return render_template(
        'index.html',
        crypto_data=crypto_data,
        cryptoData_data=cryptoData_data
    )

@app.route('/PricePage')
def PricePage():
    # Connexion à la base de données Crypto.db
    connCrypto = sqlite3.connect('Crypto.db')
    connCrypto.row_factory = sqlite3.Row

    # Récupération des données de la base
    crypto_data = connCrypto.execute('SELECT * FROM Crypto').fetchall()
    cryptoData_data = connCrypto.execute('SELECT * FROM CryptoData').fetchall()

    connCrypto.close()

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
    # Connexion à la base de données Crypto.db
    connCrypto = sqlite3.connect('Crypto.db')
    connCrypto.row_factory = sqlite3.Row

    # Récupération des données de la base
    crypto_data = connCrypto.execute('SELECT * FROM Crypto').fetchall()
    cryptoData_data = connCrypto.execute('SELECT * FROM CryptoData').fetchall()

    connCrypto.close()

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

    figBTC.update_layout(title='Évolution du Prix du BTC', xaxis_title='Date', yaxis_title='Prix (USD)')
    figETH.update_layout(title='Évolution du Prix du ETH', xaxis_title='Date', yaxis_title='Prix (USD)')
    figUDST.update_layout(title='Évolution du Prix du UDST', xaxis_title='Date', yaxis_title='Prix (USD)')
    figSOL.update_layout(title='Évolution du Prix du SOL', xaxis_title='Date', yaxis_title='Prix (USD)')
    figBNB.update_layout(title='Évolution du Prix du BNB', xaxis_title='Date', yaxis_title='Prix (USD)')

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
