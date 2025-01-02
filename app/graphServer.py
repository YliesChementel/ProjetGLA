import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from collections import defaultdict
from flask import Flask, render_template
from .DbConnexion import get_crypto_data
import plotly.graph_objects as go

# Fonction pour créer les graphiques de prix
def createPriceGraph(cryptoData_data, crypto_id):
    date = defaultdict(list)
    price = defaultdict(list)

    for data in cryptoData_data:
        price[crypto_id].append(data['price'])
        date[crypto_id].append(data['fetchTime'])

    fig = go.Figure(
        data=[go.Scatter(x=date[crypto_id], y=price[crypto_id], name=f"Prix {crypto_id}")],
        layout={'title': f"Évolution du Prix du {crypto_id}", 'xaxis': {'title': 'Date'}, 'yaxis': {'title': 'Prix (USD)'}}
    )
    return fig

# Fonction pour créer les graphiques de volume
def createVolumeGraph(cryptoData_data, crypto_id):
    date = defaultdict(list)
    volume = defaultdict(list)

    for data in cryptoData_data:
        volume[crypto_id].append(data['volume'])
        date[crypto_id].append(data['fetchTime'])

    fig = go.Figure(
        data=[go.Scatter(x=date[crypto_id], y=volume[crypto_id], name=f"Volume {crypto_id}")],
        layout={'title': f"Évolution du Volume du {crypto_id}", 'xaxis': {'title': 'Date'}, 'yaxis': {'title': 'Volume'}}
    )
    return fig

# Fonction pour créer les graphiques en chandeliers
def createCandlestickGraph(cryptoData_data, crypto_id):
    date = defaultdict(list)
    open_price = defaultdict(list)
    high_price = defaultdict(list)
    low_price = defaultdict(list)
    close_price = defaultdict(list)

    for data in cryptoData_data:
        date[crypto_id].append(data['fetchTime'])
        open_price[crypto_id].append(data['price'] - 50)
        close_price[crypto_id].append(data['price'])
        high_price[crypto_id].append(data['price'] + 100)
        low_price[crypto_id].append(data['price'] - 100)

    fig = go.Figure(data=[go.Candlestick(
        x=date[crypto_id],
        open=open_price[crypto_id],
        high=high_price[crypto_id],
        low=low_price[crypto_id],
        close=close_price[crypto_id],
        name=f"Chandeliers {crypto_id}"
    )])
    fig.update_layout(title=f"Graphique en Chandeliers du {crypto_id}")
    return fig

# Fonction pour créer un heatmap
def createHeatmap(cryptoData_data, crypto_id):
    price = defaultdict(list)
    date = defaultdict(list)

    for data in cryptoData_data:
        if data['crypto_id'] == crypto_id:
            price[crypto_id].append(data['price'])
            date[crypto_id].append(data['fetchTime'])

    heatmap_data = [
        [price[crypto_id][i] - price[crypto_id][i-1] if i > 0 else 0 for i in range(len(price[crypto_id]))]
    ]
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data,
        x=['1h', '24h', '7 jours'],
        y=[crypto_id],
        colorscale='Viridis',
    ))
    fig.update_layout(title=f"Heatmap du {crypto_id} - Variation des Prix")

    return fig

