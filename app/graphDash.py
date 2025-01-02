import dash
from dash import dcc, html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from collections import defaultdict
from DbConnexion import get_crypto_data

# Initialisation de l'application Dash
app = dash.Dash(__name__)

# Définir le crypto_id directement (ici 'bitcoin', mais vous pouvez changer cela selon vos besoins)
crypto_id = 'bitcoin'

# Récupérer les données pour le crypto_id spécifié
cryptoData_data = get_crypto_data(crypto_id)

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

# Fonction pour créer les graphiques en chandeliers
def createCandlestickGraph(cryptoData_data, crypto_id):
    date = defaultdict(list)
    open_price = defaultdict(list)
    high_price = defaultdict(list)
    low_price = defaultdict(list)
    close_price = defaultdict(list)

    for data in cryptoData_data:
        date[crypto_id].append(data['fetchTime'])
        
        # Utilisation des prix réels pour calculer les valeurs open, high, low, close
        open_price[crypto_id].append(data['price'] - 50)  # Exemple d'écart pour "open"
        close_price[crypto_id].append(data['price'])  # Prix de clôture
        high_price[crypto_id].append(data['price'] + 100)  # Exemple d'écart pour "high"
        low_price[crypto_id].append(data['price'] - 100)  # Exemple d'écart pour "low"

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

# Fonction pour créer un heatmap (exemple de variation de prix par heure)
def createHeatmap(cryptoData_data, crypto_id):
    # Initialisation des structures de données
    price = defaultdict(list)
    date = defaultdict(list)

    # Collecte des données pour le crypto_id spécifique
    for data in cryptoData_data:
        if data['crypto_id'] == crypto_id:
            price[crypto_id].append(data['price'])
            date[crypto_id].append(data['fetchTime'])

    # Exemple de calcul des variations par heure, ou autre période.
    heatmap_data = [
        [price[crypto_id][i] - price[crypto_id][i-1] if i > 0 else 0 for i in range(len(price[crypto_id]))]
    ]
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data,  # Valeurs des variations de prix
        x=['1h', '24h', '7 jours'],  # Plages horaires ou périodes spécifiques
        y=[crypto_id],  # Uniquement pour la cryptomonnaie sélectionnée
        colorscale='Viridis',  # Choix du color scale
    ))
    fig.update_layout(title=f"Heatmap du {crypto_id} - Variation des Prix")

    return fig

# Layout de la page Dash
app.layout = html.Div([
    html.H1(f"Page de Visualisation de {crypto_id.capitalize()}"),
    dcc.Dropdown(
        id='time-range-dropdown',
        options=[
            {'label': '1h', 'value': '1h'},
            {'label': '24h', 'value': '24h'},
            {'label': '7 jours', 'value': '7 jours'},
            {'label': '30 jours', 'value': '30 jours'},
        ],
        value='24h',  # Valeur par défaut
        style={'width': '50%'}
    ),
    dcc.Graph(id='price-graph'),
    dcc.Graph(id='candlestick-graph'),
    dcc.Graph(id='heatmap-graph')
])

# Callback pour mettre à jour les graphiques
@app.callback(
    [Output('price-graph', 'figure'),
     Output('candlestick-graph', 'figure'),
     Output('heatmap-graph', 'figure')],
    [Input('time-range-dropdown', 'value')]
)
def update_graphs(time_range): 
    # Récupérer les données pour la cryptomonnaie sélectionnée
    cryptoData_data = get_crypto_data(crypto_id)  # Vous pouvez ajouter la gestion du time_range ici si nécessaire

    price_graph = createPriceGraph(cryptoData_data, crypto_id)
    candlestick_graph = createCandlestickGraph(cryptoData_data, crypto_id)
    heatmap_graph = createHeatmap(cryptoData_data, crypto_id)
    
    return price_graph, candlestick_graph, heatmap_graph

# Lancer l'application
if __name__ == '__main__':
    app.run_server(debug=True)
