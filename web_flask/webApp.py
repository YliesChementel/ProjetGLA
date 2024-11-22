from flask import Flask, render_template
import sqlite3
import plotly.graph_objects as go

app = Flask(__name__)

@app.route('/')
def index():
    connCrypto = sqlite3.connect('Crypto.db')  
    
    connCrypto.row_factory = sqlite3.Row
    
    crypto_data = connCrypto.execute('SELECT * FROM Crypto').fetchall()
    cryptoData_data = connCrypto.execute('SELECT * FROM CryptoData').fetchall()
 
    connCrypto.close()
    
    prices = graphPrices(cryptoData_data)

    graphPriceBTC = prices[0].to_html(full_html=False)
    graphPriceETH = prices[1].to_html(full_html=False)
    graphPriceUDST = prices[2].to_html(full_html=False)
    graphPriceSOL = prices[3].to_html(full_html=False)
    graphPriceBNB = prices[4].to_html(full_html=False)
    
    return render_template('index.html', crypto_data=crypto_data,cryptoData_data=cryptoData_data,
    graphPriceBTC=graphPriceBTC,
    graphPriceETH=graphPriceETH,
    graphPriceUDST=graphPriceUDST,
    graphPriceSOL=graphPriceSOL,
    graphPriceBNB=graphPriceBNB)

def graphPrices(cryptoData_data):
    datesBTC = []
    datesETH = []
    datesUSDT = []
    datesSOL = []
    datesBNB = []
    pricesBTC = []
    pricesETH = []
    pricesUSDT = []
    pricesSOL= []
    pricesBNB = []
    
    for data in cryptoData_data:##C'est la même date pour toutes les donnnées donc peut-être changer ça
        if(data['crypto_id']=="bitcoin"):
            datesBTC.append(data['fetchTime'])
            pricesBTC.append(data['price'])
        if(data['crypto_id']=="ethereum"):
            datesETH.append(data['fetchTime'])
            pricesETH.append(data['price'])
        if(data['crypto_id']=="tether"):
            datesUSDT.append(data['fetchTime'])
            pricesUSDT.append(data['price'])
        if(data['crypto_id']=="solana"):
            datesSOL.append(data['fetchTime'])
            pricesSOL.append(data['price'])
        if(data['crypto_id']=="binance-coin"):
            datesBNB.append(data['fetchTime'])
            pricesBNB.append(data['price'])

    # Création du graphique
    figBTC = go.Figure()
    figETH = go.Figure()
    figUDST = go.Figure()
    figSOL = go.Figure()
    figBNB = go.Figure()

    # Ajout d'une trace
    figBTC.add_trace(go.Scatter(x=datesBTC, y=pricesBTC, mode='lines+markers', name='Prix Bitcoin'))
    figETH.add_trace(go.Scatter(x=datesETH, y=pricesETH, mode='lines+markers', name='Prix Ethereum'))
    figUDST.add_trace(go.Scatter(x=datesUSDT, y=pricesUSDT, mode='lines+markers', name='Prix Tether'))
    figSOL.add_trace(go.Scatter(x=datesSOL, y=pricesSOL, mode='lines+markers', name='Prix Solana'))
    figBNB.add_trace(go.Scatter(x=datesBNB, y=pricesBNB, mode='lines+markers', name='Prix BNB'))

    # Titres et labels
    figBTC.update_layout(
        title='Évolution du Prix du BTC',
        xaxis_title='Date',
        yaxis_title='Prix (USD)',
    )
    figETH.update_layout(
        title='Évolution du Prix du ETH',
        xaxis_title='Date',
        yaxis_title='Prix (USD)',
    )
    figUDST.update_layout(
        title='Évolution du Prix du UDST',
        xaxis_title='Date',
        yaxis_title='Prix (USD)',
    )
    figSOL.update_layout(
        title='Évolution du Prix du SOL',
        xaxis_title='Date',
        yaxis_title='Prix (USD)',
    )
    figBNB.update_layout(
        title='Évolution du Prix du BNB',
        xaxis_title='Date',
        yaxis_title='Prix (USD)',
    )

    return figBTC,figETH,figUDST,figSOL,figBNB
   

if __name__ == '__main__':
    app.run(debug=True)