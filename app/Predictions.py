import pandas as pd

# Exemple de données de prix
data = pd.Series([100, 105, 110, 120, 130, 125, 115, 105, 100, 95])

# Calcul de la moyenne mobile sur 3 jours
sma = data.rolling(window=3).mean()
print(sma)
