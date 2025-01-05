from collections import defaultdict
from flask import Flask, render_template
from .DbConnexion import get_crypto_data
from .Predictions import *
import plotly.graph_objects as go
from collections import defaultdict

def createCryptoGraph(cryptoData_data, crypto_id, graph_type):
    date = defaultdict(list)
    data_values = defaultdict(list)

    # Remplir les données en fonction du type de graphique
    for data in cryptoData_data:
        date[crypto_id].append(data['fetchTime'])
        if graph_type == 'price':
            data_values[crypto_id].append(data['price'])
        elif graph_type == 'volume':
            data_values[crypto_id].append(data['volume'])
        else:
            raise ValueError("graph_type doit être 'price' ou 'volume'.")

    # Définir le titre et l'axe Y en fonction du type de graphique
    if graph_type == 'price':
        title = f"Évolution du Prix du {crypto_id}"
        yaxis_title = 'Prix (USD)'
    elif graph_type == 'volume':
        title = f"Évolution du Volume du {crypto_id}"
        yaxis_title = 'Volume'

    # Création du graphique avec Plotly
    fig = go.Figure(
        data=[go.Scatter(x=date[crypto_id], y=data_values[crypto_id], name=f"{graph_type.capitalize()} {crypto_id}")],
        layout={
            'title': title,
            'yaxis': {'title': yaxis_title},
            'xaxis': {
                'showticklabels': False,  # Masquer les étiquettes de l'axe des X
                'showgrid': False,        # Masquer la grille de l'axe des X 
                'zeroline': False         # Masquer la ligne zéro de l'axe des X 
            }
        }
    )
    return fig


def createPredictGraph(cryptoData_data, crypto_id):
    price = [data['price'] for data in cryptoData_data]
    date = [data['fetchTime'] for data in cryptoData_data]

    if not price or not date:
        raise ValueError(f"Aucune donnée disponible pour le crypto_id {crypto_id} dans la plage de temps sélectionnée.")

    # Calculer les prévisions de la moyenne mobile
    sma = calculate_sma(price, window=5)  # Utilisation d'une fenêtre de 5 jours pour la SMA

    # Calculer la régression linéaire
    model, predictions = calculate_linear_regression(price, date)

    # Créer le graphique des prédictions
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=date, y=price, mode='lines', name='Prix Réel', line=dict(color='blue', dash='dot')))
    fig.add_trace(go.Scatter(x=date, y=sma, mode='lines', name='Moyenne Mobile (5 jours)', line=dict(color='orange')))
    fig.add_trace(go.Scatter(x=date, y=predictions.flatten(), mode='lines', name='Régression Linéaire', line=dict(color='green')))
    
    fig.update_layout(
        title=f"Prévisions du {crypto_id}",
        xaxis={
            'title': 'Date',
            'showticklabels': False, 
            'showgrid': False,
            'zeroline': False    
        },
        yaxis={'title': 'Prix (USD)'},
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
    fig.update_layout(
        title=f"Graphique en Chandeliers du {crypto_id}",
        xaxis={
            'showticklabels': False,
            'showgrid': False,       
            'zeroline': False  
        }
    )
    return fig

# Fonction pour créer un heatmap
def createHeatmap(cryptoData_data, crypto_id):
    price = defaultdict(list)
    date = defaultdict(list)

    for data in cryptoData_data:
        if data['crypto_id'] == crypto_id:
            price[crypto_id].append(data['price'])
            date[crypto_id].append(data['fetchTime'])

    heatmap_data = [[
        price[crypto_id][i] - price[crypto_id][i-1] if i > 0 else 0
        for i in range(1, len(price[crypto_id]))
    ]]
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data,
        x=[f'Variations {i+1}' for i in range(len(price[crypto_id]))],  # Affichage des Variations de données
        y=[crypto_id],
        colorscale='Viridis',
    ))
    fig.update_layout(
        title=f"Heatmap du {crypto_id} - Variation des Prix",
        xaxis={
            'showticklabels': False,  
            'showgrid': False,       
            'zeroline': False        
        }
    )

    return fig

