from collections import defaultdict
import plotly.graph_objects as go

def createPriceGraph(cryptoData_data, nbCrypto):
    # Initialisation des structures de données
    noms = []
    date = defaultdict(list)
    price = defaultdict(list)

    # Collecte des données
    for data in cryptoData_data:
        crypto_id = data['crypto_id']
        
        if crypto_id not in noms:
            noms.append(crypto_id)
        
        price[crypto_id].append(data['price'])
        date[crypto_id].append(data['fetchTime'])

    # Paramètres communs pour les graphiques
    common_layout = {
        'xaxis': {'title': 'Date'},
        'yaxis': {'title': 'Prix (USD)'},
        'hovermode': 'closest',
        'showlegend': True,
        'font': {'family': 'Arial', 'size': 12, 'color': 'black'},
        'modebar': {'remove': ['zoom', 'pan', 'resetScale', 'zoomIn', 'zoomOut', 'sendDataToCloud']},
    }

    # Création des graphiques pour les prix
    figsPrice = [
        go.Figure(
            data=[go.Scatter(x=date[crypto_id], y=price[crypto_id], name=f"Prix {crypto_id}")],
            layout={**common_layout, 'title': f"Évolution du Prix du {crypto_id}"}
        )
        for crypto_id in noms[:nbCrypto]
    ]
    
    return figsPrice

def createVolumeGraph(cryptoData_data, nbCrypto):
    # Initialisation des structures de données
    noms = []
    date = defaultdict(list)
    volume = defaultdict(list)

    # Collecte des données
    for data in cryptoData_data:
        crypto_id = data['crypto_id']
        
        if crypto_id not in noms:
            noms.append(crypto_id)
        
        volume[crypto_id].append(data['volume'])
        date[crypto_id].append(data['fetchTime'])

    # Paramètres communs pour les graphiques
    common_layout = {
        'xaxis': {'title': 'Date'},
        'yaxis': {'title': 'Prix (USD)'},
        'hovermode': 'closest',
        'showlegend': True,
        'font': {'family': 'Arial', 'size': 12, 'color': 'black'},
        'modebar': {'remove': ['zoom', 'pan', 'resetScale', 'zoomIn', 'zoomOut', 'sendDataToCloud']},
    }
    
    # Création des graphiques pour les volumes
    figsVolumes = [
        go.Figure(
            data=[go.Scatter(x=date[crypto_id], y=volume[crypto_id], name=f"Volume du {crypto_id}")],
            layout={**common_layout, 'title': f"Évolution du Volume du {crypto_id}", 'yaxis': {'title': 'Volume'}}
        )
        for crypto_id in noms[:nbCrypto]
    ]
    
    return figsVolumes


def listGraphPrice(cryptoData_data, nbCrypto):
    price = createPriceGraph(cryptoData_data, nbCrypto)
    
    listGraph = []

    for i in range(0,nbCrypto):
        graphPrice = price[i].to_html(full_html=False)
        listGraph.append(graphPrice)

    return listGraph

def listGraphVolume(cryptoData_data, nbCrypto):
    volumes = createVolumeGraph(cryptoData_data, nbCrypto)
    
    listGraph = []

    for i in range(0,nbCrypto):
        graphvolume = volumes[i].to_html(full_html=False)
        listGraph.append(graphvolume)

    return listGraph

