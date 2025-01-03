from sklearn.linear_model import LinearRegression
import numpy as np


def calculate_sma(prices, window=5):
    sma = []
    for i in range(len(prices)):
        if i + 1 >= window:
            sma.append(np.mean(prices[i+1-window:i+1]))
        else:
            sma.append(None)
    return sma

def calculate_linear_regression(prices, dates):
    # Convertir les dates en format numérique (timestamp) pour la régression linéaire
    dates_numeric = np.array([i for i in range(len(dates))]).reshape(-1, 1)  # Utilisation d'un index numérique pour les dates
    prices_numeric = np.array(prices).reshape(-1, 1)

    model = LinearRegression()
    model.fit(dates_numeric, prices_numeric)
    
    # Prédire les valeurs futures
    predictions = model.predict(dates_numeric)
    
    return model, predictions